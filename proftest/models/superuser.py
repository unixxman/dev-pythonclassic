from proftest import db
from flask_security import UserMixin
from flask_security.utils import hash_password
from .base_model import BaseModel
from .role import roles_to_superusers


class Superuser(BaseModel, UserMixin):
    __tablename__ = 'superusers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean())
    roles = db.orm.relationship(
        'Role',
        secondary=roles_to_superusers,
        back_populates='superusers',
        lazy=True)

    def __repr__(self):
        return f'{self.name}'


@db.event.listens_for(Superuser.password, 'set', retval=True)
def hash_admin_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return hash_password(value)
    return value
