import os
import logging
import sqlalchemy as db
from flask import Flask
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from flask_admin import Admin
from flask_security import Security
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from flask_cors import CORS
from flask_mail import Mail
from pathlib import Path

from .config import Config
from .admin_view import AdminView

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

#dedicated_db_engine = create_engine(f'postgresql://{Config.DEDICATED_DATABASE_USER}:{Config.DEDICATED_DATABASE_PASSWORD}@{Config.DEDICATED_DATABASE_HOST}/{Config.DEDICATED_DATABASE_NAME}')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager()

docs = FlaskApiSpec()

admin = Admin(subdomain='admin')
security = Security()

cors = CORS(resources={
    r"/*": {"origins": Config.ALLOWED_ORIGINS}
})

mail = Mail()

from .admin_panel.utils import user_datastore


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .models import Assessment

    class AssessmentAdminView(AdminView):
        def __init__(self, *args, **kwargs):
            super(AssessmentAdminView, self).__init__(*args, **kwargs)
            self.static_folder = 'static'
            self.endpoint = 'admin'
            self.name = 'Assessment'

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='proftest',
            version='v1',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/swagger/'
    })

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

    from .users.views import users
    from .assessment.views import assessment
    from .admin_panel.views import admin_panel
    from .scm.hooks import scm

    app.register_blueprint(users)
    app.register_blueprint(assessment)
    app.register_blueprint(admin_panel)
    app.register_blueprint(scm, subdomain='scm')

    docs.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    admin.init_app(app, index_view=AssessmentAdminView(
        Assessment, session, url='/panel'))
    security.init_app(app, user_datastore)

    return app


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s:%(name)s:%(levelname)s:%(message)s')

log_dir = f'{Path(__file__).parents[1]}/log'

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_handler = logging.FileHandler(f'{log_dir}/proftest.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
