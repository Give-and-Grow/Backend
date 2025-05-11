# Backend/app/models/opportunity_participant.py
import enum

from sqlalchemy import Enum, event
from sqlalchemy.sql import func

from ..extensions import db
from app.models.opportunity import Opportunity  
from app.models.volunteer_opportunity import VolunteerOpportunity


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
    org_rating = db.Column(db.Integer)
    rating = db.Column(db.Integer)  
    completed = db.Column(db.Boolean, default=False)
    points_earned = db.Column(db.Integer, default=0)
    feedback = db.Column(db.Text)
    attendance_status = db.Column(
        Enum(AttendanceStatus), default=AttendanceStatus.attended
    )
    rated_at = db.Column(db.DateTime)
    opportunity = db.relationship('Opportunity', back_populates='participants')
    
    def __repr__(self):
        return f"<OpportunityParticipant {self.id}>"

    def to_dict(self):
        opportunity_data = {
            "id": self.opportunity.id,
            "title": self.opportunity.title,
            "description": self.opportunity.description,
            "location": self.opportunity.location,
            "latitude": self.opportunity.latitude,
            "longitude": self.opportunity.longitude,
            "opportunity_type": self.opportunity.opportunity_type.value if self.opportunity.opportunity_type else None,
            "status": self.opportunity.status.value if self.opportunity.status else None,
            "start_date": self.opportunity.start_date.strftime("%Y-%m-%d") if self.opportunity.start_date else None,
            "end_date": self.opportunity.end_date.strftime("%Y-%m-%d") if self.opportunity.end_date else None,
            "created_at": self.opportunity.created_at.strftime("%Y-%m-%dT%H:%M:%S") if self.opportunity.created_at else None,
            "application_link": self.opportunity.application_link,
            "contact_email": self.opportunity.contact_email,
            "image_url": self.opportunity.image_url,
            "is_deleted": self.opportunity.is_deleted,
            "organization_id": self.opportunity.organization_id,
            
        }

        return {
            "id": self.id,
            "opportunity_id": self.opportunity_id,
            "user_id": self.user_id,
            "attendance_status": self.attendance_status.value if self.attendance_status else None,
            "completed": self.completed,
            "joined_at": self.joined_at.strftime("%Y-%m-%dT%H:%M:%S") if self.joined_at else None,
            "points_earned": self.points_earned,
            "org_rating": self.org_rating,
            "rating": self.rating,
            "feedback": self.feedback,
            "rated_at": self.rated_at.strftime("%Y-%m-%dT%H:%M:%S") if self.rated_at else None,
            "user": {
                "id": self.user.id,
                "name": self.user.name,
                "last_name": self.user.last_name,
                "profile_picture": self.user.profile_picture,
            },
            "opportunity": opportunity_data
        }


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
    
    volunteer_opportunity = db.session.query(VolunteerOpportunity).filter_by(opportunity_id=target.opportunity_id).first()
    base_points = volunteer_opportunity.base_points if volunteer_opportunity else 100  

    status = (
        target.attendance_status.value
        if target.attendance_status
        else "absent"
    )
    attendance_percentage = attendance_points_map.get(status, 0)
    attendance_score = (attendance_percentage / 100) * (0.4 * base_points)

    rating_score = 0
    if target.org_rating is not None:
        rating_score = (target.org_rating / 5) * (0.6 * base_points)

    target.points_earned = int(attendance_score + rating_score)
