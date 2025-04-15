from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from datetime import date
from ..models.account import Role

class UpdateUserProfileSchema(Schema):
    username = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    phone_number = fields.Str(required=False, allow_none=True)
    gender = fields.Str(required=False, allow_none=True)
    date_of_birth = fields.Date(required=False, allow_none=True)
    city = fields.Str(required=False, allow_none=True)
    village = fields.Str(required=False, allow_none=True)
    bio = fields.Str(required=False, allow_none=True)
    profile_picture = fields.Str(required=False, allow_none=True)
    experience = fields.Str(required=False, allow_none=True)
    identity_picture = fields.Str(required=False, allow_none=True)
    skills = fields.List(fields.Str(), required=False, allow_none=True)

    @validates('gender')
    def validate_gender(self, value):
        if value and value.lower() not in ['male', 'female', 'other']:
            raise ValidationError("Gender must be 'male', 'female', or 'other'")

class UpdateOrgProfileSchema(Schema):
    username = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=False)
    description = fields.Str(required=False, allow_none=True)
    phone = fields.Str(required=False, allow_none=True)
    logo = fields.Str(required=False, allow_none=True)
    address = fields.Str(required=False, allow_none=True)

class UpdateAdminProfileSchema(Schema):
    username = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=False, allow_none=True)
    role_level = fields.Str(required=False)

from marshmallow import Schema, fields, validates_schema, ValidationError

class ChangePasswordSchema(Schema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
    confirm_new_password = fields.Str(required=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if old_password == new_password:
            raise ValidationError("New password must be different from old password", field_name="new_password")

        if new_password != confirm_new_password:
            raise ValidationError("Password confirmation does not match", field_name="confirm_new_password")
