# Backend/app/models/report.py
from enum import Enum
from ..extensions import db


from sqlalchemy.sql import func


class ReportStatus(Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    REJECTED = "rejected"


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(
        db.Integer, db.ForeignKey("account.id"), nullable=False
    )
    reported_type = db.Column(
        db.String(50)
    ) 
    reported_id = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.Enum(ReportStatus), default=ReportStatus.PENDING)
    created_at = db.Column(db.DateTime, server_default=func.now())
