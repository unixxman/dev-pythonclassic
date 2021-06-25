from marshmallow import Schema, fields
from .answer_schema import AnswerSchema
from .submission_schema import SubmissionSchema


class QuestionSchema(Schema):
    id = fields.Integer()
    type = fields.String()
    text = fields.String()
    answers = fields.Nested(AnswerSchema, many=True)
    submission = fields.Nested(SubmissionSchema)
    unit_tests = fields.Nested(SubmissionSchema, many=True)
    other_solutions = fields.Nested(SubmissionSchema, many=True, dump_only=True)
