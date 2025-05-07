#Backend/app/schemas/opportunity_participant_schema.py
from marshmallow import Schema, fields, validate
from app.schemas.user_schema import UserDetailsShortSchema  


class RatingInputSchema(Schema):
    rating = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    feedback = fields.String(required=False, allow_none=True)
    attendance_status = fields.String(
        required=True,
        validate=validate.OneOf(["attended", "absent", "late", "excused"])
    )

class OpportunityParticipantOutputSchema(Schema):
    id = fields.Int()
    user = fields.Nested(UserDetailsShortSchema)
    rating = fields.Int()
    completed = fields.Bool()
    points_earned = fields.Int()
    attendance_status = fields.Str()
    joined_at = fields.DateTime()