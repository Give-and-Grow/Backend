# Backend/app/models/job_opportunity.py
from ..extensions import db

class JobOpportunity(db.Model):
    __tablename__ = "job_opportunity"

    job_id = db.Column(
        db.Integer, primary_key=True, unique=True
    )
    opportunity_id = db.Column(
        db.Integer, db.ForeignKey("opportunity.id"), unique=True, nullable=False
    )
    required_points = db.Column(db.Integer)

    def __repr__(self):
        return f"<JobOpportunity {self.job_id or self.opportunity_id}>"
