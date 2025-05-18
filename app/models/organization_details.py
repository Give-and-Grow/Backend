# Backend/app/models/organization_details.py

import enum
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from ..extensions import db


# ✅ Verification Status Enum
class VerificationStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


# 🏢 Organization Details Model
class OrganizationDetails(db.Model):
    __tablename__ = "organization_details"

    # 🆔 Basic Info
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("account.id"), unique=True, nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    logo = db.Column(db.String(255), nullable=True)

    # 📞 Contact Info
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)

    # 📄 Verification
    is_active = db.Column(db.Boolean, default=True)
    proof_image = db.Column(db.String(255), nullable=True)
    proof_verification_status = db.Column(
        db.Enum(VerificationStatus),
        default=VerificationStatus.PENDING,
        nullable=False
    )

    # 📆 Timestamps
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # 🔗 Relationships
    industries = db.relationship(
        "Industry",
        secondary="organization_industry",
        backref="organizations",
        lazy=True,
    )
    opportunities = db.relationship("Opportunity", backref="organization", lazy=True)

    # 🧾 String Representation
    def __repr__(self):
        return f"<OrganizationDetails {self.name}>"
