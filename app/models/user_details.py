from ..extensions import db
from sqlalchemy import Date, Enum
import enum

class VerificationStatus(enum.Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.Enum(Gender), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    village = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.Text, nullable=True)
    identity_picture = db.Column(db.String(255), nullable=True)
    identity_verification_status = db.Column(db.Enum(VerificationStatus), default=VerificationStatus.PENDING)

    skills = db.relationship('Skill', secondary='user_skills', backref=db.backref('users', lazy='dynamic'))
    
    def __repr__(self):
        return f'<UserDetails {self.name} {self.last_name}>'