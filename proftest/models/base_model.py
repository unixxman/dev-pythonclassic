from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from proftest import db, Base, session


class BaseModel(Base):
    __abstract__ = True
    created_at = db.Column(
        db.DateTime(), nullable=False,
        default=datetime.utcnow())
    updated_at = db.Column(
        db.DateTime(), nullable=False,
        default=datetime.utcnow())
    metainfo = db.Column(db.String())

    def save(self):
        try:
            session.add(self)
            session.commit()
        except (SQLAlchemyError, DBAPIError):
            session.rollback()
            raise

    def update(self, **kwargs):
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            self.updated_at = datetime.utcnow()
            session.commit()
        except (SQLAlchemyError, DBAPIError):
            session.rollback()
            raise
