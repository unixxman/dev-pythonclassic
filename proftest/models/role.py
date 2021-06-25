from enum import Enum
from proftest import db, Base
from .base_model import BaseModel


class RoleType(Enum):
    service_role = 1
    user_role = 2


roles_to_users = db.Table(
    'roles_to_users', Base.metadata,
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
)

roles_to_superusers = db.Table(
    'roles_to_superusers', Base.metadata,
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('superuser_id', db.Integer, db.ForeignKey('superusers.id')),
)


class Role(BaseModel):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    type = db.Column(db.Enum(RoleType), nullable=False)
    users = db.orm.relationship(
        'User',
        secondary=roles_to_users,
        back_populates='roles',
        lazy=True)
    superusers = db.orm.relationship(
        'Superuser',
        secondary=roles_to_superusers,
        back_populates='roles',
        lazy=True)

    def __repr__(self):
        return f'{self.name}'
