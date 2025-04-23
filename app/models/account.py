# Backend/app/models/account.py
import enum

from bcrypt import gensalt, hashpw
from sqlalchemy import DateTime, Enum
from sqlalchemy.sql import func

from ..extensions import db


class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    ORGANIZATION = "organization"


class Account(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=True, index=True)
    role = db.Column(db.Enum(Role), nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), index=True, nullable=True)
    verification_code_expiry = db.Column(
        db.DateTime(timezone=True), nullable=True
    )
    created_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now()
    )
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    last_login = db.Column(db.DateTime, nullable=True)

    organization_details = db.relationship(
    "OrganizationDetails", backref="account", uselist=False
    )
    


    def set_password(self, password):
        self.password = hashpw(password.encode("utf-8"), gensalt()).decode(
            "utf-8"
        )

    def __repr__(self):
        return f"<Account {self.username or self.email}>"
