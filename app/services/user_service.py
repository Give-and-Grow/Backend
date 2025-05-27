from sqlalchemy import func
from app.models.user_details import UserDetails, VerificationStatus
from app.models.participant_attendance import ParticipantAttendance
from app.models.user_points import UserPoints
from app.models.user_achievement import Level, Ranking

class UserService:

    @staticmethod
    def get_user_profile_summary(user_id):
        user = UserDetails.query.filter_by(account_id=user_id).first()
        if not user:
            return {"message": "User not found"}, 404

        # Points
        total_points = user.total_points or 0

        # Attendance (commitment)
        total_attendances = 0
        present_attendances = 0
        for opportunity in user.opportunities:
            print(f"Processing opportunity: {opportunity.id} for user: {user.id}")
            for attendance in opportunity.attendance_records:
                total_attendances += 1
                if attendance.status.name.lower() in ["present", "late"]:
                    present_attendances += 1

        attendance_rate = (
            round(present_attendances / total_attendances, 2) if total_attendances > 0 else 0.0
        )



        return {
            "user_id": user.id,
            "full_name": f"{user.first_name} {user.last_name}",
            "verification_status": user.identity_verification_status.value,
            "total_points": total_points,
            "attendance_rate": attendance_rate,
            "top_ranking":user.rank,
        }
