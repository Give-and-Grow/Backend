#Backend/app/models/opportunity_day.py
from ..extensions import db
import enum

from sqlalchemy import DateTime
from sqlalchemy.sql import func
from app.models.volunteer_opportunity import VolunteerOpportunity
from app.models.opportunity import Opportunity  


class WeekDay(enum.Enum):
    SUNDAY = "sunday"
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"

class OpportunityDay(db.Model):
    __tablename__ = "opportunity_day"

    id = db.Column(db.Integer, primary_key=True)
    volunteer_opportunity_id = db.Column(
        db.Integer, db.ForeignKey("volunteer_opportunity.id", ondelete="CASCADE"), nullable=False
    )
    day_of_week = db.Column(db.Enum(WeekDay), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('volunteer_opportunity_id', 'day_of_week', name='uq_volunteeropportunity_day'),
    )   

    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<OpportunityDay {self.day_of_week.value} for Opportunity {self.volunteer_opportunity_id}>"
