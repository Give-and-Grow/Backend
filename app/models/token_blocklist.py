#Backend/app/models/token_blocklist.py
from datetime import datetime, timezone

from app.extensions import db


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))