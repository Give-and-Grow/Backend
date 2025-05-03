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


class OpportunityService:

    @staticmethod
    def rate_participant(current_user_id, participant_id, data):
        # جلب بيانات المشاركة
        participant = OpportunityParticipant.query.get(participant_id)
        if not participant:
            return {"msg": "Participant not found"}, 404

        # جلب الفرصة المرتبطة بالمشاركة
        opportunity = Opportunity.query.get(participant.opportunity_id)
        if not opportunity or opportunity.is_deleted:
            return {"msg": "Opportunity not found or it has been deleted"}, 404

        # التحقق أن الحساب الحالي هو مؤسسة
        current_account = Account.query.get(current_user_id)
        if not current_account or current_account.role != Role.ORGANIZATION:
            return {"msg": "Only an organization can rate participants"}, 403

        # التحقق من أن المؤسسة هي صاحبة الفرصة
        organization_details = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
        if not organization_details or opportunity.organization_id != organization_details.id:
            return {"msg": "Unauthorized to rate this participant"}, 403

        # التحقق أن المشارك لم يتم تقييمه مسبقًا
        if participant.completed:
            return {"msg": "Participant already rated"}, 400

        # استلام بيانات التقييم
        rating = data.get("rating")
        feedback = data.get("feedback")
        attendance_status = data.get("attendance_status")

        if rating is None or attendance_status is None:
            return {"msg": "Rating and attendance status are required"}, 400

        # تعديل بيانات المشارك
        participant.rating = rating
        participant.feedback = feedback
        participant.attendance_status = AttendanceStatus(attendance_status)
        participant.rated_at = datetime.utcnow()
        participant.completed = True

        # حساب النقاط المكتسبة
        participant = OpportunityService.calculate_participant_points(participant)

        db.session.commit()

        return {
            "msg": "Participant rated successfully",
            "points_earned": participant.points_earned,
        }, 200

    @staticmethod
    def calculate_participant_points(participant):
        # جلب النقاط الأساسية من الفرصة
        volunteer_opportunity =VolunteerOpportunity.query.filter_by(opportunity_id = participant.opportunity_id).first()
        base_points = volunteer_opportunity.base_points if volunteer_opportunity else 100


        # حساب نقاط الحضور
        status = participant.attendance_status.value if participant.attendance_status else "absent"
        attendance_percentage = attendance_points_map.get(status, 0)
        attendance_score = (attendance_percentage / 100) * (0.4 * base_points)

        # حساب نقاط التقييم
        rating_score = 0
        if participant.rating is not None:
            rating_score = (participant.rating / 5) * (0.6 * base_points)

        participant.points_earned = int(attendance_score + rating_score)
        return participant

    @staticmethod
    def get_participants_by_opportunity(opportunity_id):
        opportunity = Opportunity.query.get_or_404(opportunity_id)

        # تحقق أن المستخدم هو صاحب المؤسسة
        current_user_id = get_jwt_identity()
        organization = OrganizationDetails.query.filter_by(account_id=current_user_id).first()
        if not organization or opportunity.organization_id != organization.id:
            abort(403, "You do not have permission to view this opportunity's participants.")

        participants = OpportunityParticipant.query.filter_by(opportunity_id=opportunity_id).all()
        return OpportunityParticipantOutputSchema(many=True).dump(participants)