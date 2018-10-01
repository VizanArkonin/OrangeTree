"""
Web service module.
Provides the REST API layer for interacting with application and it's sub-modules.
Uses Flask micro-framework as main workhorse.
"""
from datetime import timedelta
from threading import Thread

from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore
from database.connector import db_session, init_db
from database.models import Users, Role

# First, we initialize Flask application itself, injecting SQLAlchemy binding to provide user data for Flask-Security
web_service = Flask(__name__, static_url_path='', static_folder="../static", template_folder="../templates")
web_service.config['DEBUG'] = False
web_service.config['SECRET_KEY'] = 'super-secret'
web_service.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
web_service.config['SECURITY_PASSWORD_SALT'] = '$2a$06$6sSyl34Zw.48NBXwGBSURO'
web_service.permanent_session_lifetime = timedelta(minutes=10)
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                Users, Role)
security = Security(web_service, user_datastore)

# Then we import modules with routes
import web.general
import web.gpio_service

"""
Once done, we run the web service. We run it threaded, to prevent process lock on main level.
We do not wrap thread in abort-able loop or Daemon thread,
since we intend it to work constantly until process is terminated.
"""
service = Thread(target=web_service.run, kwargs={"host": "0.0.0.0"})
service.start()

