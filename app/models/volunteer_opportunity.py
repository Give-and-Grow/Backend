# Backend/app/models/volunteer_opportunity.py
import enum

from sqlalchemy import DateTime
from sqlalchemy.sql import func

from ..extensions import db

class VolunteerOpportunity(db.Model):
    __tablename__ = "volunteer_opportunity"
    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunity.id"), unique=True, nullable=False
    )
    max_participants = db.Column(db.Integer)
    base_points = db.Column(db.Integer, default=100)
    current_participants = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<VolunteerOpportunity {self.name or self.id}>"
