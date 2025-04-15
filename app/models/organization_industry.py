from ..extensions import db

organization_industry = db.Table('organization_industry',
    db.Column('organization_id', db.Integer, db.ForeignKey('organization_details.id'), primary_key=True),
    db.Column('industry_id', db.Integer, db.ForeignKey('industry.id'), primary_key=True)
)