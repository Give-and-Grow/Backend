from app.models.opportunity_participant import OpportunityParticipant, AttendanceStatus, attendance_points_map
from app.models.opportunity import Opportunity
from app.models.account import Account, Role
from app.models.organization_details import OrganizationDetails
from app.models.volunteer_opportunity import VolunteerOpportunity
from app.models.user_details import UserDetails
from app.extensions import db
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from app.schemas.opportunity_participant_schema import OpportunityParticipantOutputSchema
from app.schemas.user_schema import UserDetailsShortSchema
from flask import abort
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

class OpportunityService:

    @staticmethod
    def rate_participant(current_user_id, participant_id, data):
        participant = OpportunityParticipant.query.get(participant_id)
        if not participant:
            return {"msg": "Participant not found"}, 404

        opportunity = Opportunity.query.get(participant.opportunity_id)
        if not opportunity or opportunity.is_deleted:
            return {"msg": "Opportunity not found or it has been deleted"}, 404

        current_account = Account.query.get(current_user_id)
        if not current_account or current_account.role != Role.ORGANIZATION:
            return {"msg": "Only an organization can rate participants"}, 403

        organization_details = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
        if not organization_details or opportunity.organization_id != organization_details.id:
            return {"msg": "Unauthorized to rate this participant"}, 403

        if participant.completed:
            return {"msg": "Participant already rated"}, 400

        rating = data.get("rating")
        feedback = data.get("feedback")
        attendance_status = data.get("attendance_status")

        if rating is None or attendance_status is None:
            return {"msg": "Rating and attendance status are required"}, 400

        participant.rating = rating
        participant.feedback = feedback
        participant.attendance_status = AttendanceStatus(attendance_status)
        participant.rated_at = datetime.utcnow()
        participant.completed = True

        participant = OpportunityService.calculate_participant_points(participant)

        db.session.commit()

        return {
            "msg": "Participant rated successfully",
            "points_earned": participant.points_earned,
        }, 200

    @staticmethod
    def calculate_participant_points(participant):
        volunteer_opportunity =VolunteerOpportunity.query.filter_by(opportunity_id = participant.opportunity_id).first()
        base_points = volunteer_opportunity.base_points if volunteer_opportunity else 100


        status = participant.attendance_status.value if participant.attendance_status else "absent"
        attendance_percentage = attendance_points_map.get(status, 0)
        attendance_score = (attendance_percentage / 100) * (0.4 * base_points)

        rating_score = 0
        if participant.rating is not None:
            rating_score = (participant.rating / 5) * (0.6 * base_points)

        participant.points_earned = int(attendance_score + rating_score)
        return participant

    @staticmethod
    def get_participants_by_opportunity(opportunity_id):
        opportunity = Opportunity.query.get_or_404(opportunity_id)

        current_user_id = get_jwt_identity()
        organization = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
        if not organization or opportunity.organization_id != organization.id:
            return {"msg": "You do not have permission to view this opportunity's participants."}, 403

        participants = OpportunityParticipant.query.filter_by(opportunity_id=opportunity_id).all()
        schema = OpportunityParticipantOutputSchema(many=True)
        return schema.dump(participants), 200  # رجّع البيانات فقط بدون jsonify

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
            print(opportunity.start_date)
            print(datetime.utcnow().date())
            return {"msg": "Opportunity has already started"}, 400

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

        participant = OpportunityParticipant(
            opportunity_id=opportunity_id,
            user_id=user_id
        )
        db.session.add(participant)
        # زيادة عدد المشاركين الحاليين
        volunteer_opportunity.current_participants += 1
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
        return {"msg": "Withdrawn successfully"}, 200
    @staticmethod
    def check_participation(account_id, opportunity_id):
        user_details = UserDetails.query.filter_by(account_id=account_id).first()
        if not user_details:
            return {"msg": "User profile not found"}, 404
        user_id = user_details.id

        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity or opportunity.is_deleted:
            return {"msg": "Opportunity not found or deleted"}, 404

        participant = OpportunityParticipant.query.filter_by(
            opportunity_id=opportunity_id,
            user_id=user_id
        ).first()

        if participant:
            return {"msg": "User is participating in this opportunity", "is_participating": True}, 200
        else:
            return {"msg": "User is not participating in this opportunity", "is_participating": False}, 200