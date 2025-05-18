# Backend/app/schemas/password_schema.py
from marshmallow import Schema, ValidationError, fields, validates
import string


class PasswordValidationSchema(Schema):
    password = fields.Str(required=True)

    @validates("password")
    def validate_password(self, value):
        errors = []
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long")
        if not any(char.isupper() for char in value):
            errors.append("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            errors.append("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in value):
            errors.append("Password must contain at least one digit")
        if not any(char in string.punctuation for char in value):
            errors.append("Password must contain at least one special character")

        if errors:
            raise ValidationError(errors)
