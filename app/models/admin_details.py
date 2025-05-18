# Backend/app/models/admin_details.py

import enum
from sqlalchemy.sql import func
from ..extensions import db

# Enum to define admin roles
class AdminRoleLevel(enum.Enum):
    ADMIN = "admin"
    SUPERADMIN = "superadmin"
    MODERATOR = "moderator"

# AdminDetails model
class AdminDetails(db.Model):
    __tablename__ = "admin_details"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # One-to-one link with Account table
    account_id = db.Column(
        db.Integer,
        db.ForeignKey("account.id"),
        unique=True,
        nullable=False
    )

    # Admin info
    name = db.Column(db.String(100), nullable=False)
    role_level = db.Column(
        db.Enum(AdminRoleLevel),
        default=AdminRoleLevel.ADMIN,
        nullable=False
    )
    is_active = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<Admin {self.name} ({self.role_level.value})>"
