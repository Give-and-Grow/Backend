# Backend/app/models/opportunity.py
import enum
from sqlalchemy.sql import func
from ..extensions import db

class OpportunityStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    FILLED = "filled"

class OpportunityType(enum.Enum):
    VOLUNTEER = "volunteer"
    JOB = "job"

class Opportunity(db.Model):
    __tablename__ = "opportunity"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organization_details.id"), nullable=False
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    latitude = db.Column(db.Float, nullable=True)        
    longitude = db.Column(db.Float, nullable=True) 
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(
        db.Enum(OpportunityStatus), default=OpportunityStatus.OPEN
    )
    image_url = db.Column(db.String(255))
    application_link = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    opportunity_type = db.Column(db.Enum(OpportunityType), nullable=False) 
    is_deleted = db.Column(db.Boolean, default=False)  

    created_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now()
    )

    tags = db.relationship(
        "Tag", secondary="opportunity_tags", backref="opportunities"
    )
    skills = db.relationship(
        "Skill", secondary="opportunity_skills", backref="opportunities"
    )
    participants = db.relationship(
        "OpportunityParticipant", back_populates="opportunity"
    )

    volunteer_details = db.relationship(
        "VolunteerOpportunity", backref="opportunity", uselist=False
    )
    job_details = db.relationship(
        "JobOpportunity", backref="opportunity", uselist=False
    )

    def __repr__(self):
        return f"<Opportunity {self.id or self.organization_id}>"
