# Backend/app/models/industry.py
from sqlalchemy.sql import func

from ..extensions import db


class Industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Industry {self.name}>"
