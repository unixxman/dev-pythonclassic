from proftest import db, Base


association = db.Table(
    'association', Base.metadata,
    db.Column('answer_id', db.Integer, db.ForeignKey('answers.id')),
    db.Column('submission_id', db.Integer, db.ForeignKey('submissions.id')),
)
