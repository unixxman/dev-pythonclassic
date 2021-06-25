from proftest import db
from .base_model import BaseModel


class Category(BaseModel):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey(
        'assessments.id'), nullable=False)
    scope = db.Column(db.String(500), nullable=False)
    beginning = db.Column(db.String(1000), nullable=False)
    developing = db.Column(db.String(1000), nullable=False)
    accomplished = db.Column(db.String(1000), nullable=False)
    questions = db.orm.relationship(
        'Question', cascade='all, delete',
        backref='category', lazy=True)

    def __repr__(self):
        return f'{self.scope}'
