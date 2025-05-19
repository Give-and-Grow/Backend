from app.models.opportunity_participant import OpportunityParticipant, ParticipantStatus
from app.models.opportunity_rating import OpportunityRating
from app.models.participant_attendance import ParticipantAttendance
from app.extensions import db
from app.models.opportunity import Opportunity,OpportunityStatus
from app.utils.schedule_utils import check_schedule_conflict
from app.models.user_details import UserDetails
from app.models.volunteer_opportunity import VolunteerOpportunity
from datetime import datetime, timedelta,date

class UserParticipantService:
    @staticmethod
    def join_opportunity(account_id, opportunity_id):
        user_details = UserDetails.query.filter_by(account_id=account_id).first()
        if not user_details:
            return {"msg": "User profile not found"}, 404
        user_id = user_details.id

        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity or opportunity.is_deleted:
            return {"msg": "Opportunity not found or deleted"}, 404

        if opportunity.start_date <= datetime.utcnow().date():
            return {"msg": "Opportunity has already started"}, 400
        if opportunity.status in [OpportunityStatus.CLOSED, OpportunityStatus.FILLED]:
            return {"msg": "This opportunity is not open for applications"}, 400
        existing = OpportunityParticipant.query.filter_by(
            opportunity_id=opportunity_id,
            user_id=user_id
        ).first()
        if existing:
            return {"msg": "Already joined this opportunity"}, 400

        volunteer_opportunity = VolunteerOpportunity.query.filter_by(opportunity_id=opportunity_id).first()
        if not volunteer_opportunity:
            return {"msg": "Volunteer settings not found"}, 404

        current_count = OpportunityParticipant.query.filter_by(opportunity_id=opportunity_id).count()
        if current_count >= volunteer_opportunity.max_participants:
            return {"msg": "Volunteer limit reached"}, 400

        # التحقق من وجود تعارض في الجدول الزمني
        if check_schedule_conflict(user_id, opportunity):
            return {"msg": "Schedule conflict with another opportunity"}, 400

        participant = OpportunityParticipant(
            opportunity_id=opportunity_id,
            user_id=user_id
        )
        db.session.add(participant)
        volunteer_opportunity.current_participants += 1
        if volunteer_opportunity.current_participants >= volunteer_opportunity.max_participants:
            opportunity.status = OpportunityStatus.FILLED
        db.session.commit()

        return {"msg": "Joined successfully"}, 200

  
    @staticmethod
    def withdraw_from_opportunity(account_id, opportunity_id):
        user_details = UserDetails.query.filter_by(account_id=account_id).first()
        if not user_details:
            return {"msg": "User profile not found"}, 404
        user_id = user_details.id

        participant = OpportunityParticipant.query.filter_by(
            opportunity_id=opportunity_id,
            user_id=user_id
        ).first()
        if not participant:
            return {"msg": "You are not registered in this opportunity"}, 404

        if participant.status != ParticipantStatus.PENDING:
            return {"msg": "Cannot withdraw after being accepted or rejected"}, 400

        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return {"msg": "Opportunity not found"}, 404

        if opportunity.start_date - timedelta(days=1) <= datetime.utcnow().date():
            return {"msg": "Cannot withdraw within 1 day of the opportunity"}, 400

        volunteer_opportunity = VolunteerOpportunity.query.filter_by(opportunity_id=opportunity_id).first()
        if volunteer_opportunity and volunteer_opportunity.current_participants > 0:
            volunteer_opportunity.current_participants -= 1

        db.session.delete(participant)
        db.session.commit()

        return {"msg": "Application withdrawn successfully"}, 200


    @staticmethod
    def get_user_applications(account_id):
        user_details = UserDetails.query.filter_by(account_id=account_id).first()
        if not user_details:
            return {"msg": "User profile not found"}, 404

        user_id = user_details.id
        applications = OpportunityParticipant.query.filter_by(user_id=user_id).all()
        result = []

        for app in applications:
            opportunity = Opportunity.query.get(app.opportunity_id)

            has_attended = ParticipantAttendance.query.filter_by(
                participant_id=app.id,
                status="present"
            ).first() is not None

            already_evaluated = OpportunityRating.query.filter_by(
                participant_id=app.id
            ).first() is not None

            is_ended = opportunity.end_date and opportunity.end_date <= date.today()

            can_evaluate = is_ended and has_attended and not already_evaluated

            result.append({
                "id": app.id,
                "user_id": app.user_id,
                "opportunity_id": app.opportunity_id,
                "status": app.status.value,
                "applied_at": app.applied_at.isoformat(),
                "can_evaluate": can_evaluate,
                "opportunity": {
                    "id": opportunity.id,
                    "title": opportunity.title,
                    "description": opportunity.description,
                    "start_date": opportunity.start_date.isoformat() if opportunity.start_date else None,
                    "end_date": opportunity.end_date.isoformat() if opportunity.end_date else None,
                    "status": opportunity.status.value,
                    "location": opportunity.location,
                },
                "organization": {
                    "id": opportunity.organization_id,
                    "name": opportunity.organization.name,
                    "logo": opportunity.organization.logo,
                },
            })

        return result


    @staticmethod
    def evaluate_participation(account_id, participant_id, rating, feedback):
        user_details = UserDetails.query.filter_by(account_id=account_id).first()
        if not user_details:
            return {"error": "User profile not found."}, 404
        user_id = user_details.id

        participant = OpportunityParticipant.query.get(participant_id)
        if not participant or participant.user_id != user_id:
            return {"error": "Participation not found."}, 404

        opportunity = Opportunity.query.get(participant.opportunity_id)
        if not opportunity:
            return {"error": "Opportunity not found."}, 404

        if not opportunity.end_date or opportunity.end_date > date.today():
            return {"error": "You can only evaluate after the opportunity ends."}, 403

        attendance = ParticipantAttendance.query.filter_by(
            participant_id=participant_id,
            status="present"
        ).first()

        if not attendance:
            return {"error": "You must have attended to evaluate this opportunity."}, 403

        existing = OpportunityRating.query.filter_by(participant_id=participant_id).first()
        if existing:
            return {"error": "You have already evaluated this opportunity."}, 400

        if not (1 <= rating <= 5):
            return {"error": "Rating must be between 1 and 5."}, 400

        evaluation = OpportunityRating(
            participant_id=participant_id,
            rating=rating,
            comment=feedback
        )
        db.session.add(evaluation)
        db.session.commit()

        return {
            "message": "Evaluation submitted successfully.",
            "evaluation": {
                "participant_id": evaluation.participant_id,
                "rating": evaluation.rating,
                "comment": evaluation.comment
            }
        }
