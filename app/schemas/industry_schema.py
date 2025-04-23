#Backend/app/schemas/industry_schema.py
from marshmallow import Schema, fields


class IndustrySchema(Schema):
    id = fields.Int()
    name = fields.Str()
