#Backend/app/models/participant_evaluation.py
from ..extensions import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class ParticipantEvaluation(db.Model):
    __tablename__ = "participant_evaluation"
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("opportunity_participant.id"), nullable=False)
    opportunity_day_id = db.Column(db.Integer, db.ForeignKey("opportunity_day.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    opportunity_day = db.relationship("OpportunityDay", backref="evaluations")
    participant = db.relationship("OpportunityParticipant", back_populates="evaluations")
