# Backend/app/models/user_points.py
from ..extensions import db


class UserPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_details.id"), nullable=False
    )
    total_points = db.Column(db.Integer, default=0)
    month = db.Column(db.String(7))  
    year = db.Column(db.Integer)
