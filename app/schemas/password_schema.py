# backend/app/schemas/password_schema.py
from marshmallow import Schema, fields, validates, ValidationError
import re

class PasswordValidationSchema(Schema):
    password = fields.Str(required=True)

    @validates("password")
    def validate_password(self, value):
        if not re.search(r"[A-Z]", value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValidationError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError("Password must contain at least one special character")
