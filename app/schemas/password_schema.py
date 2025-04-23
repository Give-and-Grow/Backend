#Backend/app/schemas/password_schema.py
from marshmallow import Schema, ValidationError, fields, validates


class PasswordValidationSchema(Schema):
    password = fields.Str(required=True)

    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long"
            )
        if not any(char.isupper() for char in value):
            raise ValidationError(
                "Password must contain at least one uppercase letter"
            )
        if not any(char.islower() for char in value):
            raise ValidationError(
                "Password must contain at least one lowercase letter"
            )
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one digit")
