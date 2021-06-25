from datetime import datetime
from proftest import db
from .base_model import BaseModel
from .assosociation import association


class Submission(BaseModel):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'questions.id'), nullable=False)
    time_submitted = db.Column(db.DateTime, default=datetime.utcnow())
    value = db.Column(db.JSON, nullable=True)
    rating = db.Column(db.Integer, default=0)
    purpose = db.Column(db.String(15), nullable=False)
    answers = db.orm.relationship(
        'Answer', secondary=association,
        back_populates='submissions', lazy=True
    )
