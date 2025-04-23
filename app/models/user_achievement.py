# Backend/app/models/user_achievement.py
import enum
from datetime import datetime, timedelta

from sqlalchemy import DateTime, Enum, func
from sqlalchemy.sql import func

from ..extensions import db


class Type(enum.Enum):
    MONTH = "month"
    SMONTH = "smonths"
    YEAR = "year"


class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_details.id"), nullable=False
    )
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    badge_icon = db.Column(db.String(255))
    period_type = db.Column(db.Enum(Type), nullable=False)
    period_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now()
    )
