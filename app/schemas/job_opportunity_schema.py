from marshmallow import Schema, fields

class JobOpportunitySchema(Schema):
    required_points = fields.Integer()
