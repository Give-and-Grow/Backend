from marshmallow import Schema, fields, validate, EXCLUDE, validates, ValidationError
from marshmallow.validate import Length
from app.models.opportunity import OpportunityStatus, OpportunityType
from app.schemas.skill_schema import SkillSchema
from app.schemas.tag_schema import TagSchema
from app.schemas.volunteer_opportunity_schema import VolunteerOpportunitySchema
from app.schemas.job_opportunity_schema import JobOpportunitySchema

class OpportunitySchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=Length(min=3, max=255))
    description = fields.String(required=True, validate=Length(min=10))
    location = fields.String(validate=Length(min=3, max=255))
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    status = fields.String(validate=validate.OneOf(["open", "closed", "filled"]), missing="open")
    image_url = fields.String(validate=Length(min=3, max=255))
    application_link = fields.String(validate=Length(min=5, max=255))
    contact_email = fields.Email(required=True)
    opportunity_type = fields.String(validate=validate.OneOf(["volunteer", "job"]), required=True)
    created_at = fields.DateTime(dump_only=True)
    skills = fields.Nested(SkillSchema, many=True)
    tags = fields.Nested(TagSchema, many=True)
    tags = fields.List(fields.Integer())  # tags optional
    skills = fields.List(fields.Integer(), required=True)  # skills mandatory

    max_participants = fields.Integer(required=False)
    base_points = fields.Integer(required=False, default=100)
    required_points = fields.Integer(required=False)


    class Meta:
        unknown = EXCLUDE

    @validates("skills")
    def validate_skills(self, value):
        if not value or len(value) == 0:
            raise ValidationError("At least one skill is required.")


class FilterOpportunitySchema(Schema):
    opportunity_type = fields.String(validate=validate.OneOf(["volunteer", "job"]))
    status = fields.String(validate=validate.OneOf(["open", "closed", "filled"]))
    page = fields.Integer(missing=1)
    per_page = fields.Integer(missing=10)

class OpportunityPaginationSchema(Schema):
    opportunities = fields.List(fields.Nested(OpportunitySchema))
    total = fields.Integer()
    pages = fields.Integer()
    page = fields.Integer()
    per_page = fields.Integer()

class OpportunityGetSchema(Schema):
    id = fields.Int(dump_only=True)
    organization_id = fields.Int()
    title = fields.Str(required=True)
    description = fields.Str()
    location = fields.Str()
    start_date = fields.Date(required=True)
    end_date = fields.Date()
    status = fields.Str(validate=lambda x: x in [status.value for status in OpportunityStatus], missing=OpportunityStatus.OPEN.value)
    image_url = fields.Str()
    application_link = fields.Str()
    contact_email = fields.Email(required=True)
    opportunity_type = fields.Str(required=True, validate=lambda x: x in [o.value for o in OpportunityType])
    volunteer_info = fields.Nested(VolunteerOpportunitySchema, dump_only=True)
    job_info = fields.Nested(JobOpportunitySchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)