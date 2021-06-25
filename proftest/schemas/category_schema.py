from marshmallow import Schema, fields
from .question_schema import QuestionSchema


class CategorySchema(Schema):
    id = fields.Integer()
    scope = fields.String()
    beginning = fields.String()
    developing = fields.String()
    accomplished = fields.String()
    questions = fields.Nested(QuestionSchema, many=True)
