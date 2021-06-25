from flask import g
from sqlalchemy.orm.exc import NoResultFound
from proftest import db
from .base_model import BaseModel
from .submission import Submission
from .category import Category


class Question(BaseModel):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    type = db.Column(db.String(7), nullable=False)
    text = db.Column(db.String(1500), nullable=False)
    code_placeholder = db.Column(db.String(), default='# type your code below')
    answers = db.orm.relationship(
        'Answer', cascade='all, delete',
        backref='question', lazy=True)
    submissions = db.orm.relationship(
        'Submission', cascade='all, delete',
        backref='question', lazy=True)

    __mapper_args__ = {'polymorphic_on': type}

    @property
    def submission(self):
        return Submission.query.filter(
            db.or_(
                Submission.user_id == g.user_id, Submission.user_id == None),
            Submission.question_id == self.id, Submission.purpose != 'test').\
                order_by(Submission.user_id).first()

    @property
    def unit_tests(self):
        return Submission.query.filter(
            Submission.purpose == 'test',
            Submission.question_id == self.id).order_by(db.desc(Submission.rating)).\
                limit(10).all()

    @property
    def other_solutions(self):
        return Submission.query.filter(
            Submission.user_id != g.user_id,
            Submission.purpose == 'source',
            Submission.question_id == self.id).order_by(db.desc(Submission.rating)).\
                limit(100).all()

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
        if kwargs['type'] == 'coding':
            submission = Submission(value={'code': self.code_placeholder}, purpose='source')
            self.submissions.append(submission)

    def __repr__(self):
        return f'{self.text}'

    @classmethod
    def get(cls, question_id, assessment_id):
        try:
            return cls.query.filter(
                cls.id == question_id
            ).join(Category).filter(
                Category.assessment_id == assessment_id
            ).one()
        except NoResultFound:
            raise ValueError('No questions found')
