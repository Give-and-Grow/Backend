# Backend/app/models/opportunity_tags.py
from ..extensions import db

opportunity_tags = db.Table(
    "opportunity_tags",
    db.Column(
        "opportunity_id",
        db.Integer,
        db.ForeignKey("opportunity.id"),
        primary_key=True,
    ),
    db.Column(
        "tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True
    ),
)
