from threading import Thread
from flask import Blueprint, current_app, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from proftest import docs
from proftest.models import User
from proftest.schemas import UserSchema, AuthSchema
from proftest.base_view import BaseView
from .utils import Notifier

users = Blueprint('users', __name__)


class RegisterView(BaseView):
    @use_kwargs(UserSchema)
    @marshal_with(AuthSchema)
    def post(self, **kwargs):
        try:
            user = User(**kwargs)
            user.save()
            token = user.get_token()
            notifier = Notifier()
            thread = Thread(
                target=notifier.send_registration_email, args=[user])
            thread.start()
            return {'access_token': token}
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise Exception('User exists')
            else:
                raise


class LoginView(BaseView):
    @use_kwargs(UserSchema(only=('email', 'password')))
    @marshal_with(AuthSchema)
    def post(self, **kwargs):
        user = User.authenticate(**kwargs)
        token = user.get_token()
        return {'access_token': token}


class ProfileView(BaseView):
    @jwt_required
    @marshal_with(UserSchema)
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user


class ConfirmEmailView(BaseView):
    @jwt_required
    @use_kwargs(AuthSchema)
    @marshal_with(UserSchema)
    def post(self, **kwargs):
        g.user_id = get_jwt_identity()
        user = User.verify_confirm_token(
            kwargs.get('confirm_token'),
            current_app.config['SECRET_KEY'])
        if not user:
            raise PermissionError(
                f'user:{g.user_id} email confirmation failed. Token is invalid')
        user.update(email_confirmed=True)
        return user


RegisterView.register(users, docs, '/register', 'registerview')
LoginView.register(users, docs, '/login', 'loginview')
ProfileView.register(users, docs, '/profile', 'profileview')
ConfirmEmailView.register(users, docs, '/email-confirm', 'confirmemailview')
