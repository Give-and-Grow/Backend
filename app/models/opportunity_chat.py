from app.extensions import db
from sqlalchemy.sql import func

class OpportunityChat(db.Model):
    __tablename__ = "opportunity_chat"
    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey("opportunity.id"), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    opportunity = db.relationship("Opportunity", back_populates="chat")
