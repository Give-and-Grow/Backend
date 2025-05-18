# Backend/app/models/follow.py

from datetime import datetime
from ..extensions import db

# Follow model: represents user-to-user follows
class Follow(db.Model):
    __tablename__ = "follows"

    # Composite Primary Key: follower and followed
    follower_id = db.Column(
        db.Integer,
        db.ForeignKey("account.id"),
        primary_key=True
    )
    followed_id = db.Column(
        db.Integer,
        db.ForeignKey("account.id"),
        primary_key=True
    )

    # Timestamp when the follow happened
    followed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationships
    follower_account = db.relationship(
        "Account",
        foreign_keys=[follower_id],
        back_populates="following"
    )
    followed_account = db.relationship(
        "Account",
        foreign_keys=[followed_id],
        back_populates="followers"
    )
