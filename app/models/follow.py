from datetime import datetime
from ..extensions import db
from app.models.account import Account, Role
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key=True)
    followed_at = db.Column(db.DateTime, default=datetime.utcnow)

    follower_account = db.relationship('Account', foreign_keys=[follower_id], back_populates='following')
    followed_account = db.relationship('Account', foreign_keys=[followed_id], back_populates='followers')