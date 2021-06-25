from marshmallow import Schema, fields
from .category_schema import CategorySchema
from .feedback_schema import FeedbackSchema


class AssessmentSchema(Schema):
    id = fields.Integer()
    topic = fields.String()
    description = fields.String()
    average_duration = fields.Integer()
    level = fields.Method('get_level')
    candidates_num = fields.Integer()

    def get_level(self, obj):
        return obj.level.name


class AssessmentDetailedSchema(Schema):
    id = fields.Integer()
    topic = fields.String()
    description = fields.String()
    average_duration = fields.Integer()
    categories = fields.Nested(CategorySchema, many=True)
    feedback = fields.Nested(FeedbackSchema, dump_only=True)
