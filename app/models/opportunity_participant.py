# Backend/app/models/opportunity_participant.py
import enum

from sqlalchemy import Enum, event
from sqlalchemy.sql import func

from ..extensions import db
from app.models.opportunity import Opportunity  # تأكد من استيراد الموديل


class AttendanceStatus(enum.Enum):
    attended = "attended"
    absent = "absent"
    late = "late"
    excused = "excused"


class OpportunityParticipant(db.Model):
    __tablename__ = "opportunity_participant"

    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunity.id"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_details.id"), nullable=False
    )
    joined_at = db.Column(db.DateTime, server_default=func.now())
    rating = db.Column(db.Integer)  # تقييم من 1 إلى 5
    completed = db.Column(db.Boolean, default=False)
    points_earned = db.Column(db.Integer, default=0)
    feedback = db.Column(db.Text)
    attendance_status = db.Column(
        Enum(AttendanceStatus), default=AttendanceStatus.attended
    )
    rated_at = db.Column(db.DateTime)
    user = db.relationship('Account', back_populates='participants')
    opportunity = db.relationship('Opportunity', back_populates='participants')


# توزيع النقاط:
# 40% على الالتزام بالحضور
# 60% على التقييم
attendance_points_map = {
    "attended": 100,
    "late": 70,
    "excused": 50,
    "absent": 0,
}


@event.listens_for(OpportunityParticipant, "before_insert")
@event.listens_for(OpportunityParticipant, "before_update")
def calculate_points(mapper, connection, target):
    # جلب النقاط الأساسية من الفرصة
    opportunity = db.session.get(Opportunity, target.opportunity_id)
    base_points = (
        opportunity.base_points if opportunity else 100
    )  # القيمة الافتراضية 100

    # حساب نقاط الحضور
    status = (
        target.attendance_status.value
        if target.attendance_status
        else "absent"
    )
    attendance_percentage = attendance_points_map.get(status, 0)
    attendance_score = (attendance_percentage / 100) * (0.4 * base_points)

    # حساب نقاط التقييم
    rating_score = 0
    if target.rating is not None:
        rating_score = (target.rating / 5) * (0.6 * base_points)

    target.points_earned = int(attendance_score + rating_score)
