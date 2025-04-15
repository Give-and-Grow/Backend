import enum
from ..extensions import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class VerificationStatus(enum.Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class OrganizationDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    logo = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    proof_image = db.Column(db.String(255), nullable=True)
    proof_verification_status = db.Column(db.Enum(VerificationStatus), default=VerificationStatus.PENDING)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    industries = db.relationship('Industry', secondary='organization_industry', backref='organizations', lazy=True)

    def __repr__(self):
        return f'<OrganizationDetails {self.name}>'