# Backend/app/schemas/organization_schema.py
from marshmallow import Schema, fields, validate
from marshmallow.validate import Length, Regexp, URL

from app.models.organization_details import VerificationStatus
from app.schemas.industry_schema import IndustrySchema


class OrganizationUpdateSchema(Schema):
    name = fields.String(
        required=False,
        validate=Length(min=2, max=255)
    )
    description = fields.String(required=False)
    
    phone = fields.String(
        required=False,
        validate=[
            Length(max=20),
            Regexp(r"^\+?[0-9\s\-]+$", error="Invalid phone number format")
        ]
    )
    
    address = fields.String(required=False)
    
    logo = fields.String(
        required=False,
        validate=URL(relative=False, schemes={"http", "https"})
    )
    
    proof_image = fields.String(
        required=False,
        validate=URL(relative=False, schemes={"http", "https"})
    )

class IndustryListSchema(Schema):
    industry_ids = fields.List(
        fields.Integer(strict=True),
        required=True,
        validate=validate.Length(
            min=1, error="At least one industry ID is required."
        ),
    )

class IndustryOutputSchema(Schema):
    id = fields.Integer()
    name = fields.String()



class OrganizationProfileSchema(Schema):
    id = fields.Int()
    account_id = fields.Int()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    logo = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)
    proof_image = fields.Str(allow_none=True)
    proof_verification_status = fields.Method("get_verification_status")
    industries = fields.Nested(IndustrySchema, many=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime(allow_none=True)

    def get_verification_status(self, obj):
        return (
            obj.proof_verification_status.value
            if obj.proof_verification_status
            else None
        )
