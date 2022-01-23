from functools import wraps
from flask import g
from flask_mail import Message
from flask_jwt_extended import get_jwt_identity, get_jwt_claims
from proftest import mail
from proftest.config import Config
from proftest.models import User


"""def create_dedicated_db(**kwargs):
    user = kwargs['name']
    password = kwargs['password']
    conn = dedicated_db_engine.connect()
    try:
        conn.execute(f"CREATE USER {user} WITH PASSWORD '{password}';")

        dedicated_db_url = f'postgresql://{Config.DEDICATED_DATABASE_USER}:{Config.DEDICATED_DATABASE_PASSWORD}@{Config.DEDICATED_DATABASE_HOST}/{user}_db'
        engine = create_engine(dedicated_db_url)
        if not database_exists(engine.url):
            create_database(engine.url)
            conn.execute(f"GRANT ALL PRIVILEGES ON DATABASE {user}_db to {user};")
    except Exception as e:
        logger.error(f'user:{user} failed to dedicate database to user {e}')
    finally:
        conn.close()"""


class Notifier:

    """Class for user's notifications

    Attributes:
        send_email (function): async task which sends email
    """

    def send_email(self, subject, body, recipients):
        from proftest.wsgi import app
        with app.app_context():
            msg = Message(
                subject,
                sender=(
                    'Pythonclassic',
                    f'{Config.MAIL_USERNAME}'),
                recipients=recipients)
            msg.body = body + \
                ('\n'
                    'Спасибо, что Вы с нами\n'
                    'С уважением, команда pythonclassic')
            mail.send(msg)

    def send_registration_email(self, user):
        """Sends email when user registers

        Args:
            user (User): user instance
        """
        token = user.get_confirm_token(Config.SECRET_KEY)
        confirm_link = f'{Config.FRONTEND_URL}/confirm-email/{token}'
        body = ('Здравствуйте\n'
                'При регистрации аккаунта в приложении pythonclassic был указан Ваш Email. Если это были Вы, то перейдите по ссылке:\n'
                f'{confirm_link}')
        self.send_email(
            'Регистрация в pythonclassic',
            body, [user.email])

    def send_confirm_email(self, user):
        """Sends email when user requests email confirmation

        Args:
            user (User): user instance
        """
        token = user.get_confirm_token(Config.SECRET_KEY)
        confirm_link = f'{Config.FRONTEND_URL}/confirm-email/{token}'
        body = ('Здравствуйте\n'
                'Вы или кто то другой указал данный Email в приложении pythonclassic. Если это были Вы то перейдите по ссылке ниже:\n'
                f'{confirm_link}\n'
                'или проигнорируйте это письмо')
        self.send_email(
            'Подтверждение Email в pythonclassic',
            body, [user.email])

    def send_reset_email(self, user):
        """Sends email when user requests password reset

        Args:
            user (User): user instance
        """
        token = user.get_confirm_token(
            Config.RESET_PASSWORD_SALT)
        reset_link = f'{Config.FRONTEND_URL}/reset-password/{token}'
        body = ('Здравствуйте\n'
                'Чтобы сбросить пароль, перейдите по ссылке:\n'
                f'{reset_link}\n'
                'Если это не вы отправили запрос, просто проигнорируйте это письмо.')
        self.send_email(
            'Сброс пароля по запросу пользователя в pythonclassic',
            body, [user.email])

    def send_changepass_email(self, user):
        """Sends email when user changes password

        Args:
            user (User): user instance
        """
        body = ('Здравствуйте\n'
                'Пароль успешно изменен.')
        self.send_email(
            'Изменение пароля в pythonclassic',
            body, [user.email])


def check_identity(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not getattr(g, 'user_id', None):
            g.user_id = get_jwt_identity()
        user = User.query.get(g.user_id)
        if not user.email_confirmed:
            raise PermissionError(f'user:{g.user_id} email is not confirmed')
        return fn(g.user_id, *args, **kwargs)
    return wrapper


def set_claims(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not getattr(g, 'user_id', None):
            g.user_id = get_jwt_identity()
        g.roles = get_jwt_claims().get('roles', [])
        return fn(*args, **kwargs)
    return wrapper
