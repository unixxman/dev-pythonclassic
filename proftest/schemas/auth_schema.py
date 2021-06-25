from marshmallow import fields, validate
from .base_schema import BaseSchema


class AuthSchema(BaseSchema):
    access_token = fields.String(dump_only=True)
    confirm_token = fields.String(load_only=True)
    password = fields.String(validate=[
        validate.Length(max=100)], load_only=True)
