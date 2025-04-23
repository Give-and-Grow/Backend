# Backend/app/models/volunteer_opportunity.py
from ..extensions import db

class VolunteerOpportunity(BaseOpportunity):
    __tablename__ = "volunteer_opportunity"

    id = db.Column(
        db.Integer, db.ForeignKey("opportunity.id"), primary_key=True
    )
    max_participants = db.Column(db.Integer)
    base_points = db.Column(db.Integer, default=100)
    current_participants = db.Column(db.Integer, default=0)
    idea_id = db.Column(db.Integer, db.ForeignKey("volunteer_idea.id"))
    idea = db.relationship("VolunteerIdea", backref="opportunity")

    __mapper_args__ = {"polymorphic_identity": OpportunityType.VOLUNTEER.value}
