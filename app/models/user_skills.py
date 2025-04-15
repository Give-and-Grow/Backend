from ..extensions import db

user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user_details.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)