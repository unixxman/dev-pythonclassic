from proftest import db
from sqlalchemy.orm.exc import NoResultFound
from .base_model import BaseModel
from .assosociation import association


class Answer(BaseModel):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'questions.id'), nullable=False)
    text = db.Column(db.String(500), nullable=True)
    is_right = db.Column(db.Boolean, default=False, nullable=False)
    submissions = db.orm.relationship(
        'Submission', secondary=association,
        back_populates='answers', lazy=True
    )

    def __repr__(self):
        return f'{self.text}'

    @classmethod
    def get(cls, answer_id, question_id):
        try:
            return cls.query.filter(
                cls.id == answer_id,
                cls.question_id == question_id).one()
        except NoResultFound:
            raise ValueError('No such answer')
