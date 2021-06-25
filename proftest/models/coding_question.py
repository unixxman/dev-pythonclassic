from sqlalchemy.ext.declarative import declared_attr
from proftest import db
from proftest.assessment.utils import role_required
from .question import Question
from .submission import Submission


class CodingQuestion(Question):
    __mapper_args__ = {'polymorphic_identity': 'coding'}

    @declared_attr
    def file_name(cls):
        return Question.__table__.c.get('metainfo', db.Column(db.String))

    @role_required
    def submit(self, user_id, **kwargs):
        value = kwargs.get('value')     # TODO: validate this
        if not value:
            raise ValueError('Submit valid code')
        purpose = kwargs.get('purpose')
        submission = Submission.query.filter(
            Submission.question_id == self.id,
            Submission.user_id == user_id,
            Submission.purpose == purpose
        ).first()
        if not submission:
            submission = Submission(
                user_id=user_id,
                question_id=self.id,
                value=value,
                purpose=purpose
            )
            submission.save()
        else:
            submission.update(value=value)
