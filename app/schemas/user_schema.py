#backend/app/schemas/user_schema.py
from marshmallow import Schema, fields, validate, validates, ValidationError
from marshmallow.validate import Length, Regexp, OneOf
from datetime import date
import re


class UpdateProfileSchema(Schema):
    username = fields.Str(validate=Length(min=3, max=30))
    name = fields.Str(validate=Length(min=2, max=50))
    last_name = fields.Str(validate=Length(min=2, max=50))
    phone_number = fields.Str(validate=Regexp(r'^\+?\d{7,15}$', error="Invalid phone number"))
    gender = fields.Str(validate=OneOf(["male", "female"]))
    city = fields.Str(validate=Length(min=2, max=50))
    village = fields.Str(validate=Length(min=2, max=50))
    bio = fields.Str(validate=Length(max=250))
    experience = fields.Str(validate=Length(max=250))
    date_of_birth = fields.Date()  
    profile_picture = fields.Url(error="Invalid URL")
    identity_picture = fields.Url(error="Invalid URL")

#backend/app/schemas/user_schema.py
class ChangePasswordSchema(Schema):
    old_password = fields.Str(required=True, validate=validate.Length(min=8, max=128), error_messages={
        "required": "Old password is required",
        "invalid": "Old password must be at least 8 characters"
    })
    new_password = fields.Str(required=True, validate=validate.Length(min=8, max=128), error_messages={
        "required": "New password is required",
        "invalid": "New password must be at least 8 characters"
    })
    confirm_new_password = fields.Str(required=True, validate=validate.Length(min=8, max=128), error_messages={
        "required": "Password confirmation is required",
        "invalid": "Password confirmation must be at least 8 characters"
    })

    @validates("new_password")
    def validate_new_password(self, value):
        # تحقق من قوة كلمة المرور
        if not re.search(r"[A-Z]", value):
            raise ValidationError("New password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValidationError("New password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValidationError("New password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError("New password must contain at least one special character")

        # تحقق من عدم تطابق كلمة المرور الجديدة مع القديمة
        if value == self.context.get("old_password"):
            raise ValidationError("New password must be different from old password")

    @validates("confirm_new_password")
    def validate_confirm_new_password(self, value):
        # تحقق من تطابق كلمة المرور الجديدة مع التأكيد
        if value != self.context.get("new_password"):
            raise ValidationError("New password and confirmation do not match")
