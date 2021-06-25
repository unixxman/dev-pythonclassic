from marshmallow import fields, validate
from .base_schema import BaseSchema
from .role_schema import RoleSchema


class UserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[
        validate.Length(max=63), validate.Regexp(r'^[a-zA-Z0-9_]+$')])
    email = fields.String(required=True, validate=[
        validate.Length(max=250)])
    password = fields.String(required=True, validate=[
        validate.Length(max=100)], load_only=True)
    email_confirmed = fields.Boolean(dump_only=True)
    roles = fields.Pluck(RoleSchema, 'name', many=True, dump_only=True)
