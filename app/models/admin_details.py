from ..extensions import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class AdminDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    role_level = db.Column(db.String(50), default='admin')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<AdminDetails {self.name or self.account_id}>'