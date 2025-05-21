from marshmallow import Schema, fields, validates_schema, ValidationError, validate
from app.models.opportunity import OpportunityType, OpportunityStatus
from app.models.opportunity_day import WeekDay

class OpportunitySchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str()
    location = fields.Str()
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    status = fields.Str(validate=validate.OneOf([s.value for s in OpportunityStatus]), missing="open")
    image_url = fields.Url()
    application_link = fields.Url()
    contact_email = fields.Email(required=True)
    opportunity_type = fields.Str(required=True, validate=validate.OneOf([t.value for t in OpportunityType]))
    
    skills = fields.List(fields.Int(), required=True)

    # Volunteer-only fields
    max_participants = fields.Int()
    base_points = fields.Int(missing=100)
    volunteer_days = fields.List(fields.Str(validate=validate.OneOf([d.value for d in WeekDay])))
    start_time = fields.Time(format="%H:%M")
    end_time = fields.Time(format="%H:%M")

    # Job-only field
    required_points = fields.Int()

    @validates_schema
    def validate_by_type(self, data, **kwargs):
        opp_type = data.get("opportunity_type")

        if opp_type == OpportunityType.VOLUNTEER.value:
            missing_fields = []
            if "max_participants" not in data:
                missing_fields.append("max_participants")
            if "volunteer_days" not in data or not data["volunteer_days"]:
                missing_fields.append("volunteer_days")
            if "start_time" not in data:
                missing_fields.append("start_time")
            if "end_time" not in data:
                missing_fields.append("end_time")
            
            if missing_fields:
                raise ValidationError(
                    {field: ["This field is required for volunteer opportunities."] for field in missing_fields}
                )
            
        elif opp_type == OpportunityType.JOB.value:
            if "required_points" not in data:
                raise ValidationError({"required_points": ["This field is required for job opportunities."]})

class OpportunityUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=3))
    description = fields.Str()
    location = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.Str(validate=validate.OneOf([s.value for s in OpportunityStatus]))
    image_url = fields.Url()
    application_link = fields.Url()
    contact_email = fields.Email()
    opportunity_type = fields.Str(validate=validate.OneOf([t.value for t in OpportunityType]))

    skills = fields.List(fields.Int())

    max_participants = fields.Int()
    base_points = fields.Int()
    volunteer_days = fields.List(fields.Str(validate=validate.OneOf([d.value for d in WeekDay])))
    start_time = fields.Time(format="%H:%M")
    end_time = fields.Time(format="%H:%M")

    required_points = fields.Int()

    @validates_schema
    def validate_by_type_if_present(self, data, **kwargs):
        opp_type = data.get("opportunity_type")
    
        if opp_type == OpportunityType.VOLUNTEER.value:
            missing_fields = []
            if "max_participants" in data and data["max_participants"] is None:
                missing_fields.append("max_participants")
            if "volunteer_days" in data and not data["volunteer_days"]:
                missing_fields.append("volunteer_days")
            if "start_time" in data and data["start_time"] is None:
                missing_fields.append("start_time")
            if "end_time" in data and data["end_time"] is None:
                missing_fields.append("end_time")

            if missing_fields:
                raise ValidationError({
                    field: ["This field is required for volunteer opportunities."] for field in missing_fields
                })

        elif opp_type == OpportunityType.JOB.value:
            if "required_points" in data and data["required_points"] is None:
                raise ValidationError({"required_points": ["This field is required for job opportunities."]})


