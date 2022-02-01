from marshmallow import fields
from .base_schema import BaseSchema
from .auth_schema import AuthSchema
from .user_schema import UserSchema
from .assessment_schema import AssessmentSchema, AssessmentDetailedSchema
from .submission_schema import SubmissionSchema
from .feedback_schema import FeedbackSchema


def create_schema(data_schema, **kwargs):
    class GenericSchema(BaseSchema):
        data = fields.Nested(data_schema, **kwargs)
    return GenericSchema
