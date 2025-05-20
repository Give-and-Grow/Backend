#Backend/app/models/opportunity_participant.py
from ..extensions import db
import enum
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from app.models.opportunity import Opportunity


class ParticipantStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class OpportunityParticipant(db.Model):
    __tablename__ = "opportunity_participant"
    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey("opportunity.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_details.id"), nullable=False)
    status = db.Column(db.Enum(ParticipantStatus), default=ParticipantStatus.PENDING)
    applied_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        db.UniqueConstraint("opportunity_id", "user_id", name="uq_opportunity_user"),
    )
    opportunity = db.relationship("Opportunity", back_populates="participants")
    user = db.relationship("UserDetails", back_populates="opportunities")
    attendance_records = db.relationship("ParticipantAttendance", back_populates="participant", cascade="all, delete-orphan")
    evaluations = db.relationship("ParticipantEvaluation", back_populates="participant", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Participant user={self.user_id} opportunity={self.opportunity_id} status={self.status.value}>"
