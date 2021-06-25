from proftest import session
from proftest.models import Superuser, Role
from flask_security import SQLAlchemySessionUserDatastore

user_datastore = SQLAlchemySessionUserDatastore(session, Superuser, Role)
