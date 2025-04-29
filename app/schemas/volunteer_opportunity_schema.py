from marshmallow import Schema, fields

class VolunteerOpportunitySchema(Schema):
    max_participants = fields.Integer()
    base_points = fields.Integer()
    current_participants = fields.Integer()
