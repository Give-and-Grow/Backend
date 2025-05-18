from ..extensions import db
from datetime import datetime

class OpportunityRating(db.Model):
    __tablename__ = 'opportunity_ratings'
    id = db.Column(db.Integer, primary_key=True)
    
    participant_id = db.Column(db.Integer, db.ForeignKey("opportunity_participant.id"), nullable=False)
    
    rating = db.Column(db.Integer, nullable=False)  
    comment = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
