import os
import json


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    # DEDICATED_DATABASE_HOST = os.environ.get('DEDICATED_DATABASE_HOST')
    # DEDICATED_DATABASE_USER = os.environ.get('DEDICATED_DATABASE_USER')
    # DEDICATED_DATABASE_PASSWORD = os.environ.get('DEDICATED_DATABASE_PASSWORD')
    # DEDICATED_DATABASE_NAME = os.environ.get('DEDICATED_DATABASE_NAME')
    ALLOWED_ORIGINS = json.loads(os.environ.get('ALLOWED_ORIGINS'))
    SERVER_NAME = os.environ.get('SERVER_NAME')
    SECURITY_PASSWORD_SALT = os.environ.get('ADMIN_PASSWORD_SALT')
    SECURITY_LOGIN_URL = '/panel/login'
    SECURITY_SUBDOMAIN = 'admin'
    GIT_ROOT = '/srv/git'
    REPO_REMOTE = os.environ.get('PUBLIC_GIT_REPO')
    REPO_NAME = 'entipy'
    GIT_SSH_KEY_PUBLIC = os.path.expanduser(
        f'~/.ssh/{os.environ.get("SSH_KEY_NAME")}.pub')
    GIT_SSH_KEY_PRIVATE = os.path.expanduser(
        f'~/.ssh/{os.environ.get("SSH_KEY_NAME")}')
    MAIL_USERNAME = os.environ.get('ADMIN_EMAIL')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    FRONTEND_URL = 'https://dev.pythonclassic.com'
