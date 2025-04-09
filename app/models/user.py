from ..extensions import db
from bcrypt import hashpw, gensalt
from sqlalchemy import DateTime
from sqlalchemy import Date
from sqlalchemy.sql import func
from datetime import (timezone,date)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)  
    gender = db.Column(db.String(10), nullable=True)  
    date_of_birth = db.Column(Date, nullable=True)  
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))  
    verification_code_expiry = db.Column(DateTime(timezone=True))

    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def __repr__(self):
        return f'<User {self.username}>'