# Backend/app/models/admin_details.py
import enum

from sqlalchemy import DateTime
from sqlalchemy.sql import func

from ..extensions import db


class AdminRoleLevel(enum.Enum):
    ADMIN = "admin"
    SUPERADMIN = "superadmin"
    MODERATOR = "moderator"


class AdminDetails(db.Model):
    __tablename__ = "admin_details"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey("account.id"), unique=True, nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    role_level = db.Column(
        db.Enum(AdminRoleLevel), default=AdminRoleLevel.ADMIN
    )
    created_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now()
    )
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<AdminDetails {self.name or self.account_id}>"
