from app.models.opportunity_participant import OpportunityParticipant, ParticipantStatus
from app.models.participant_evaluation import ParticipantEvaluation
from app.models.participant_attendance import ParticipantAttendance
from app.extensions import db
from app.models.opportunity import Opportunity,OpportunityStatus
from app.utils.schedule_utils import check_schedule_conflict
from app.models.user_details import UserDetails
from app.models.volunteer_opportunity import VolunteerOpportunity
from datetime import datetime, timedelta


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

