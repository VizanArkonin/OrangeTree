"""
Web service module.
Provides the REST API layer for interacting with application and it's sub-modules.
Uses Flask micro-framework as main workhorse.
"""
from datetime import timedelta
from threading import Thread

from flask_sqlalchemy import SQLAlchemy

from server.config import DATABASE_CONFIG

from flask import Flask, session
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_security.utils import hash_password
from flask_socketio import SocketIO

from server.config import WEB_SERVICE_CONFIG

# First, we initialize Flask application itself, SQLAlchemy and Flask-Security.
# Flask app and config
web_service = Flask(__name__, static_url_path=WEB_SERVICE_CONFIG["static_url_path"],
                    static_folder=WEB_SERVICE_CONFIG["static_files_path"],
                    template_folder=WEB_SERVICE_CONFIG["templates_path"])
socket_service = SocketIO(web_service)
web_service.config['DEBUG'] = WEB_SERVICE_CONFIG["debug"]
web_service.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONFIG["connection_string"]
web_service.config['SECRET_KEY'] = WEB_SERVICE_CONFIG["security_secret_key"]
web_service.config['SECURITY_PASSWORD_HASH'] = WEB_SERVICE_CONFIG["security_password_hash"]
web_service.config['SECURITY_PASSWORD_SALT'] = WEB_SERVICE_CONFIG["security_password_salt"]
if WEB_SERVICE_CONFIG["expire_session"]:
    session.permanent = True
    web_service.permanent_session_lifetime = timedelta(minutes=WEB_SERVICE_CONFIG["session_timeout_in_minutes"])
    web_service.config['SESSION_REFRESH_EACH_REQUEST'] = WEB_SERVICE_CONFIG["refresh_session_on_each_request"]

# Flask-SQLAlchemy
db = SQLAlchemy(web_service)
import server.database.models   # Do NOT remove this import - it pulls up all models for SQLAlchemy module.
db.create_all()

# Flask-Security
from server.database.models.user.users import Users
from server.database.models.user.roles import Roles

user_datastore = SQLAlchemySessionUserDatastore(db.session, Users, Roles)
security = Security(web_service, user_datastore)

# Then we import modules with routes
import server.web.routes

# Since we cannot properly create after_create hook for user model (it's bound to context-based Flask-Security module),
# we validate if there are any users existing. If not - we create default one by creating before_first call hook.
# TODO: Rework it to use static-file stored parameters (i.e. JSON data provider)
if len(Users.query.all()) == 0:
    @web_service.before_first_request
    def create_default_user():
        user_datastore.create_user(email="some@mail.com",
                                   password=hash_password("password"),
                                   roles=["admin", "user"])
        db.session.commit()

"""
Once done, we run the web service. We run it threaded, to prevent process lock on main level.
We do not wrap thread in abort-able loop or Daemon thread,
since we intend it to work constantly until process is terminated.
"""
service = Thread(target=web_service.run, kwargs={"host": WEB_SERVICE_CONFIG["host"],
                                                 "port": WEB_SERVICE_CONFIG["web_port"]})
socket = Thread(target=socket_service.run, args=[web_service], kwargs={"host": WEB_SERVICE_CONFIG["host"],
                                                                       "port": WEB_SERVICE_CONFIG["socket_port"]})
service.start()
socket.start()
