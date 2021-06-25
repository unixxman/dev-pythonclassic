from marshmallow import Schema, fields, validate
from .answer_schema import AnswerSchema
from .import UserSchema


class ValueSchema(Schema):
    code = fields.String(required=True)


class SubmissionSchema(Schema):
    id = fields.Integer(dump_only=True)
    time_submitted = fields.DateTime(dump_only=True)
    value = fields.Nested(ValueSchema, allow_none=True)
    rating = fields.Integer(dump_only=True)
    purpose = fields.String(validate=[
        validate.OneOf(['source', 'test', 'variant'])
    ], required=True)
    answers = fields.Pluck(AnswerSchema, 'id', many=True, allow_none=True)
    user = fields.Nested(UserSchema, dump_only=True)
