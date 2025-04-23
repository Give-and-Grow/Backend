# Backend/app/models/volunteer_idea.py
from ..extensions import db

class IdeaStatus(enum.Enum):
    PENDING = "pending"
    ADOPTED = "adopted"
    REJECTED = "rejected"


class VolunteerIdea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proposer_id = db.Column(
        db.Integer, db.ForeignKey("user_details.id"), nullable=False
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum(IdeaStatus, native_enum=False), default=IdeaStatus.PENDING
    )
    adopted_by = db.Column(
        db.Integer, db.ForeignKey("organization_details.id")
    )
    adopted_at = db.Column(db.DateTime)
    submitted_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now()
    )
