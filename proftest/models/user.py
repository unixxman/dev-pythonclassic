from passlib.hash import bcrypt
from datetime import timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_jwt_extended import create_access_token
from sqlalchemy.orm.exc import NoResultFound
from proftest import db
from proftest.schemas.role_schema import RoleSchema
from .base_model import BaseModel
from .feedback import Feedback
from .role import roles_to_users


class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    assessments = db.orm.relationship(
        'Assessment', secondary=Feedback.__table__,
        back_populates='candidates', lazy=True)
    roles = db.orm.relationship(
        'Role',
        secondary=roles_to_users,
        back_populates='users',
        lazy=True)
    submissions = db.orm.relationship('Submission', backref='user', lazy=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))

    def __repr__(self):
        return f'{self.name}'

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id,
            expires_delta=expire_delta,
            user_claims={'roles': RoleSchema(many=True).dump(self.roles)}
        )
        return token

    def get_confirm_token(self, salt, expires_sec=10800):
        s = Serializer(salt, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_confirm_token(token, salt):
        s = Serializer(salt)
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

    @classmethod
    def authenticate(cls, email, password):
        try:
            user = cls.query.filter(cls.email == email).one()
            if not bcrypt.verify(password, user.password):
                raise ValueError('No user with this password')
            return user
        except NoResultFound:
            raise ValueError('No user with this email')
