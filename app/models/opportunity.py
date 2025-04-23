# Backend/app/models/opportunity.py
import enum

from sqlalchemy.sql import func

from app import db


class OpportunityType(enum.Enum):
    VOLUNTEER = "volunteer"
    JOB = "job"


class OpportunityStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    FILLED = "filled"


class BaseOpportunity(db.Model):
    __tablename__ = "opportunity"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organization_details.id"), nullable=False
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(
        db.Enum(OpportunityStatus, native_enum=False),
        default=OpportunityStatus.OPEN,
    )
    image_url = db.Column(db.String(255))
    application_link = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=func.now())

    tags = db.relationship(
        "Tag", secondary="opportunity_tags", backref="opportunities"
    )
    skills = db.relationship(
        "Skill", secondary="opportunity_skills", backref="opportunities"
    )
    
    
    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "base"}
