from enum import Enum
from sqlalchemy.orm.exc import NoResultFound
from proftest import db
from .base_model import BaseModel


class ProficiencyLevel(Enum):
    beginning = 1
    developing = 2
    accomplished = 3


class FeedbackState(Enum):
    PENDING = 1
    PASSED = 2
    FIXED = 3
    BROKEN = 4
    FAILED = 5
    STILL_FAILING = 6
    CANCELED = 7
    ERRORED = 8


class Feedback(BaseModel):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'))
    score = db.Column(db.Integer, nullable=False)
    proficiency = db.Column(db.Enum(ProficiencyLevel), nullable=False)
    state = db.Column(db.Enum(FeedbackState))
    build_url = db.Column(db.String)

    def __str__(self):
        return f'{self.proficiency}'

    @classmethod
    def get(cls, feedbback_id, user_id):
        try:
            return cls.query.filter(
                cls.id == feedbback_id, cls.candidate_id == user_id).one()
        except NoResultFound:
            raise ValueError('No such feedback')
