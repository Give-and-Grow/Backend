# Backend/app/models/account.py

import enum
from bcrypt import gensalt, hashpw, checkpw
from sqlalchemy import DateTime, Enum
from sqlalchemy.sql import func

from ..extensions import db


# 🔑 User Roles Enum
class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    ORGANIZATION = "organization"


# 🧾 Account Model
class Account(db.Model):
    __tablename__ = "account"

    # 🆔 Identity & Authentication
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=True, index=True)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.USER)

    # 📩 Verification
    is_email_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True, index=True)
    verification_code_expiry = db.Column(db.DateTime(timezone=True), nullable=True, index=True)

    # 📆 Status & Activity
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    fcm_token = db.Column(db.String(512), nullable=True)

    # 🔗 Relationships
    organization_details = db.relationship("OrganizationDetails", backref="account", uselist=False)
    user_details = db.relationship("UserDetails", backref="account", uselist=False)
    admin_details = db.relationship("AdminDetails", backref="account", uselist=False)

    followers = db.relationship(
        'Follow',
        foreign_keys='Follow.followed_id',
        back_populates='followed_account'
    )
    following = db.relationship(
        'Follow',
        foreign_keys='Follow.follower_id',
        back_populates='follower_account'
    )

    # 🔐 Password Helpers
    def set_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.password = hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

    def check_password(self, password):
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    # 🧾 String Representation
    def __repr__(self):
        return f"<Account {self.username or self.email}>"
