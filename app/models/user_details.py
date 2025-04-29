# Backend/app/models/user_details.py
import enum

from sqlalchemy import Date, Enum
from sqlalchemy.sql import func

from ..extensions import db


class VerificationStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class UserDetails(db.Model):
    __tablename__ = "user_details"
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("account.id"), unique=True, nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.Enum(Gender), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    country = db.Column(db.String(100), nullable=True)  
    city = db.Column(db.String(100), nullable=True)
    village = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)        
    longitude = db.Column(db.Float, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.Text, nullable=True)
    identity_picture = db.Column(db.String(255), nullable=True)
    identity_verification_status = db.Column(
        db.Enum(VerificationStatus), default=VerificationStatus.PENDING
    )
    total_points = db.Column(db.Integer, default=0)
    current_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    skills = db.relationship(
        "Skill",
        secondary="user_skills",
        backref=db.backref("users", lazy="dynamic"),
    )
    achievements = db.relationship(
        "UserAchievement", backref="user", lazy=True
    )
    points = db.relationship("UserPoints", backref="user", lazy=True)

    def __repr__(self):
        return f"<UserDetails {self.name} {self.last_name}>"
