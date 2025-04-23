# Backend/app/models/job_opportunity.py
class JobOpportunity(BaseOpportunity):
    __tablename__ = "job_opportunity"

    id = db.Column(
        db.Integer, db.ForeignKey("opportunity.id"), primary_key=True
    )
    required_points = db.Column(db.Integer)

    __mapper_args__ = {"polymorphic_identity": OpportunityType.JOB.value}
