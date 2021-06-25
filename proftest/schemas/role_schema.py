from marshmallow import Schema, fields


class RoleSchema(Schema):
    name = fields.String()
