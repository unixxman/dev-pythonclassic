from marshmallow import Schema, fields, validate


class AnswerSchema(Schema):
    id = fields.Integer()
    text = fields.String(required=True, validate=[
        validate.Length(max=500)])
    is_right = fields.Boolean(required=True, load_only=True)
