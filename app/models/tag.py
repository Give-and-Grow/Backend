# Backend/app/models/tag.py
from sqlalchemy.sql import func
from ..extensions import db



class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now()
    )


opportunity_tags = db.Table(
    "opportunity_tags",
    db.Column(
        "opportunity_id",
        db.Integer,
        db.ForeignKey("opportunity.id"),
        primary_key=True,
    ),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)
