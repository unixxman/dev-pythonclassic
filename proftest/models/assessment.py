from enum import Enum
from flask import g
from proftest import db
from .base_model import BaseModel
from .feedback import Feedback
from .question import Question


class ComplexityLevel(Enum):
    beginner = 1
    intermediate = 2
    advanced = 3
    pro = 4


class Assessment(BaseModel):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    average_duration = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Enum(ComplexityLevel), nullable=False)
    public = db.Column(db.Boolean)
    candidates = db.orm.relationship(
        'User', secondary=Feedback.__table__,
        back_populates='assessments', lazy=True)
    categories = db.orm.relationship(
        'Category', cascade='all, delete',
        backref='assessment', lazy=True)

    def __repr__(self):
        return f'{self.topic}'

    @property
    def candidates_num(self):
        return len(self.candidates)

    @property
    def feedback(self):
        return Feedback.query.filter(
            Feedback.assessment_id == self.id,
            Feedback.candidate_id == g.user_id,
            Feedback.state != 'CANCELED').first()

    @staticmethod
    def get_filters():
        filters = []
        if not any(r['name'] == 'qa' for r in getattr(g, 'roles', [])):
            filters.append(Assessment.public == True)
        return filters

    @staticmethod
    def get(assessment_id):
        return Assessment.query.filter(
            *Assessment.get_filters(),
            Assessment.id == assessment_id
        ).one()

    def calculate_score(self, user_id):
        coding_question = Question.query.filter(
            Question.type == 'coding',
            Question.category.has(assessment_id=self.id)).first()
        total = 50 if coding_question else 100
        multichoice_questions = Question.query.filter(
            Question.type == 'choices',
            Question.category.has(assessment_id=self.id)).all()
        return total * sum(
            [int(q.get_candidate_solution(user_id)) for q in multichoice_questions]) \
            // len(multichoice_questions)
