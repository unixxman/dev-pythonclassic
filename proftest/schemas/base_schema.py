from marshmallow import Schema, fields


class BaseSchema(Schema):
    message = fields.String(dump_only=True)
    statusCode = fields.Integer(dump_only=True, default=0)
