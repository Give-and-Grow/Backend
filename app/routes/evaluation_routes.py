from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.participant_evaluation import ParticipantEvaluation
from app.models.opportunity_participant import OpportunityParticipant, ParticipantStatus
from app.models.opportunity import Opportunity
from app.extensions import db
from datetime import datetime
from decimal import Decimal
from app.utils.calculate_hours import calculate_volunteer_hours
from app.utils.calculate_points import calculate_participant_points
from app.utils.points import update_user_points_summary, create_or_update_achievement
from app.models.user_points import UserPoints
from app.services.notification_service import notify_user
from firebase_admin import firestore
from app.config import db_firestore 
from app.models import *

import random

evaluation_bp = Blueprint("evaluation", __name__)

def maybe_grant_discount(user):
    try:
        # Get discount codes with required points <= user total points
        discount_ref = db_firestore.collection("discount_codes")
        eligible_codes = discount_ref.where("points_required", "<=", user.total_points).stream()
        eligible_list = [doc.to_dict() for doc in eligible_codes]

        if not eligible_list:
            return  # No available discount codes

        selected_code = random.choice(eligible_list)

        notify_user(
            user_id=str(user.id),
            title="🎉 Congratulations! You’ve earned a discount code!",
            body=f"You’ve been promoted to {user.rank} rank. Enjoy a special discount from {selected_code['store_name']}!",
            data={
                "type": "discount_code",
                "img": selected_code["code"],  # image URL of the discount code
                "from": "GiveAndGrow"
            }
        )
    except Exception as e:
        print(f"Error in maybe_grant_discount: {e}")

def get_all_discount_codes():
    docs = db_firestore.collection("discount_codes").stream()
    codes = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    return jsonify(codes)

@evaluation_bp.route("/<int:opportunity_id>", methods=["GET"])
@jwt_required()
def get_participants_evaluation(opportunity_id):
    date_str = request.args.get("date")
    if not date_str:
        return jsonify({"error": "Missing date parameter"}), 400

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    opportunity = Opportunity.query.filter_by(id=opportunity_id, is_deleted=False).first()
    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    participants = OpportunityParticipant.query.filter_by(
        opportunity_id=opportunity_id,
        status=ParticipantStatus.ACCEPTED
    ).all()

    response = []
    for p in participants:
        evaluation = ParticipantEvaluation.query.filter_by(
            participant_id=p.id,
            date=date
        ).first()

        response.append({
            "participant_id": p.id,
            "user_id": p.user_id,
            "name": p.user.first_name + " " + p.user.last_name,
            "profile_picture": p.user.profile_picture,
            "phone": p.user.phone_number,
            "score": evaluation.score if evaluation else -1,
            "notes": evaluation.notes if evaluation else ""
        })

    return jsonify({
        "date": date_str,
        "participants": response
    }), 200

@evaluation_bp.route("/<int:opportunity_id>", methods=["POST"])
@jwt_required()
def post_evaluations(opportunity_id):
    try:
        data = request.get_json()
        if not data or not isinstance(data, list):
            return jsonify({"error": "Expected a list of evaluation records"}), 400

        required_fields = ["participant_id", "date", "score"]

        opportunity = Opportunity.query.filter_by(id=opportunity_id, is_deleted=False).first()
        if not opportunity:
            return jsonify({"error": "Opportunity not found"}), 404

        for record in data:
            if not all(field in record for field in required_fields):
                return jsonify({"error": f"Missing fields in record: {record}"}), 400

            participant = OpportunityParticipant.query.filter_by(
                id=record["participant_id"],
                opportunity_id=opportunity_id
            ).first()
            if not participant:
                return jsonify({"error": f"Participant {record['participant_id']} not found"}), 404

            try:
                eval_date = datetime.strptime(record["date"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": f"Invalid date format: {record['date']}. Use YYYY-MM-DD"}), 400

            score = record["score"]
            if not isinstance(score, int) or not (0 <= score <= 10):
                return jsonify({"error": f"Invalid score for participant {record['participant_id']}. Must be between 0 and 10"}), 400

            notes = record.get("notes", "")

            existing_eval = ParticipantEvaluation.query.filter_by(
                participant_id=record["participant_id"],
                date=eval_date
            ).first()

            if existing_eval:
                existing_eval.score = score
                existing_eval.notes = notes
            else:
                new_eval = ParticipantEvaluation(
                    participant_id=record["participant_id"],
                    date=eval_date,
                    score=score,
                    notes=notes
                )
                db.session.add(new_eval)

        db.session.commit()

        for record in data:
            participant_id = record["participant_id"]
            participant = OpportunityParticipant.query.get(participant_id)
            if not participant or not participant.user:
                continue

            user = participant.user

            total_points = db.session.query(
                db.func.coalesce(db.func.sum(UserPoints.points_earned), 0)
            ).filter_by(user_id=user.id).scalar()

            user.total_points = total_points

            if total_points >= 100000:
                user.rank = "Platinum"
            elif total_points >= 10000:
                user.rank = "Gold"
            elif total_points >= 1000:
                user.rank = "Silver"
            else:
                user.rank = "Bronze"

            attended_hours = round(calculate_volunteer_hours(opportunity, user.id, db.session).get("attended_hours", 0), 1)

            total_score = calculate_participant_points(participant_id, db.session)

            points = int(total_score * Decimal(str(attended_hours)))

            user_points = UserPoints.query.filter_by(
                user_id=user.id,
                opportunity_id=opportunity_id,
                date=record["date"]
            ).first()

            if user_points:
                print(f"✏️ Updating existing UserPoints for user {user.id} on {record['date']}")
                user_points.points_earned = points
            else:
                print(f"➕ Creating new UserPoints for user {user.id} on {record['date']}")
                user_points = UserPoints(
                    user_id=user.id,
                    opportunity_id=opportunity_id,
                    points_earned=points,
                    date=record["date"]
                )
                db.session.add(user_points)


            update_user_points_summary(user.id, db.session)
            create_or_update_achievement(user, db.session)
            if user.rank != old_rank:
                maybe_grant_discount(user)

        db.session.commit()

        return jsonify({"message": "Evaluations and points processed successfully", "count": len(data)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@evaluation_bp.route("/test-discount", methods=["GET"])
# @jwt_required()
def test_discount_for_user1():
    try:
        user = UserDetails.query.get(1)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # تعديل النقاط والرتبة لتجربة الترقية
        user.total_points = 5000
        user.rank = "Silver"
        db.session.commit()

        # جلب أكواد الخصم المؤهلة (نقاط المطلوبة أقل أو تساوي نقاط المستخدم)
        discount_ref = db_firestore.collection("discount_codes")
        eligible_codes = discount_ref.where("points_required", "<=", user.total_points).stream()

        eligible_list = []
        for doc in eligible_codes:
            data = doc.to_dict()
            try:
                # تأكد أن points_required رقم صحيح (لأن ممكن يكون نص)
                points_req = int(data.get("points_required", "0"))
            except ValueError:
                points_req = 0

            if points_req <= user.total_points:
                eligible_list.append(data)

        if not eligible_list:
            return jsonify({"message": "No eligible discount codes found"}), 200

        selected_code = random.choice(eligible_list)

        notify_user(
            user_id=str(39),
            title="🎉 Congratulations! You’ve earned a discount code!",
            body=f"You’ve been promoted to {user.rank} rank. Enjoy a special discount from {selected_code['store_name']}!",
            data={
                "type": "discount_code",
                "img": selected_code["code"],  
                "from": "GiveAndGrow"
            }
        )

        return jsonify({"message": "Discount code sent", "store": selected_code["store_name"]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
