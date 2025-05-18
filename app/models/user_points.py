# Backend/app/models/user_points.py
import enum
from sqlalchemy import Date
from ..extensions import db


class PeriodType(enum.Enum):
    MONTH = "month"
    SMONTH = "smonths"
    YEAR = "year"


class UserPoints(db.Model):
    __tablename__ = "user_points"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_details.id"), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey("opportunity.id"), nullable=False)
    points_earned = db.Column(db.Integer, nullable=False, default=0)

    user = db.relationship("UserDetails", back_populates="points")
    opportunity = db.relationship("Opportunity", backref="user_points")

    __table_args__ = (
        db.UniqueConstraint("user_id", "opportunity_id", name="uq_user_opportunity_points"),
    )

    def __repr__(self):
        return f"<UserPoints user={self.user_id}, opportunity={self.opportunity_id}, points={self.points_earned}>"


class UserPointsSummary(db.Model):
    __tablename__ = "user_points_summary"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_details.id"), nullable=False)

    period_type = db.Column(db.Enum(PeriodType), nullable=False)
    period_start = db.Column(Date, nullable=False)
    period_end = db.Column(Date, nullable=False)

    total_points = db.Column(db.Integer, default=0)

    user = db.relationship("UserDetails", back_populates="points_summaries")


    def __repr__(self):
        return f"<UserPointsSummary user={self.user_id}, period={self.period_type.value} from {self.period_start} to {self.period_end}>"
