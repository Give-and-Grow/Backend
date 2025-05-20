from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.participant_evaluation import ParticipantEvaluation
from app.models.opportunity_participant import OpportunityParticipant, ParticipantStatus
from app.models.opportunity import Opportunity
from app.extensions import db
from datetime import datetime

evaluation_bp = Blueprint("evaluation", __name__)

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
        return jsonify({"message": "Evaluations processed successfully", "count": len(data)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
