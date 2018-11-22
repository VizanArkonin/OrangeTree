"""
General routing library
"""

from flask import render_template
from flask_login import user_logged_in
from flask_security import login_required, roles_required, roles_accepted
from datetime import datetime

from board_controller.server import server_interface
from config import WEB_SERVICE_CONFIG
from web import web_service


@user_logged_in.connect_via(web_service)
def on_user_logged_in(sender, user):
    """
    This function is fired after user have been successfully logged in.

    :param sender: Sender instance (Flask)
    :param user: User instance
    :return: None
    """
    user.last_login_at = datetime.now()
    if user.login_count:
        user.login_count += 1
    else:
        user.login_count = 1


@web_service.route("/monitor/<string:device_id>", methods=["GET"])
@login_required
@roles_accepted("admin")
def monitor(device_id):
    """
    Maps monitor path to a static index file
    :param device_id: Device ID
    :return: Rendered template
    """
    return render_template("gpio/monitor.html",
                           pins_config=server_interface.get_device_pin_config(device_id),
                           socket_url=WEB_SERVICE_CONFIG["host"],
                           socket_port=WEB_SERVICE_CONFIG["socket_port"])


@web_service.route("/index", methods=["GET"])
@login_required
@roles_accepted("admin")
@roles_accepted("user")
def index():
    """
    Maps monitor path to a static index file
    :return: Rendered template
    """
    return render_template("general/index.html")
