# Backend/app/models/user_details.py

import enum
from sqlalchemy import Date, Enum
from sqlalchemy.sql import func
from ..extensions import db


# Enums
class VerificationStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


# Model
class UserDetails(db.Model):
    __tablename__ = "user_details"

    # 🧑‍💼 Account & Identity Info
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)

    # 📞 Contact & Location
    phone_number = db.Column(db.String(15), nullable=True)
    country = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    village = db.Column(db.String(80), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # 🪪 Verification & Identity
    identity_picture = db.Column(db.String(255), nullable=True)
    identity_verification_status = db.Column(
        db.Enum(VerificationStatus),
        default=VerificationStatus.PENDING,
        nullable=False
    )

    # 🧾 Profile Info
    bio = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.Text, nullable=True)

    # 🏆 Points & Rank
    rank = db.Column(db.String(50), nullable=True)
    total_points = db.Column(db.Integer, default=0)
    current_points = db.Column(db.Integer, default=0)

    # 🕒 Timestamps
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # 🔗 Relationships
    skills = db.relationship(
        "Skill",
        secondary="user_skills",
        backref=db.backref("users", lazy="dynamic"),
    )
    achievements = db.relationship("UserAchievement", backref="user", lazy=True)
    opportunities = db.relationship("OpportunityParticipant", back_populates="user", lazy=True)
    points = db.relationship("UserPoints", back_populates="user", cascade="all, delete-orphan")
    points_summaries = db.relationship("UserPointsSummary", back_populates="user", cascade="all, delete-orphan")
    
    

    def __repr__(self):
        return f"<UserDetails {self.first_name} {self.last_name}>"
