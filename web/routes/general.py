"""
General routing library
"""

from flask import render_template
from flask_login import user_logged_in
from flask_security import login_required, roles_required, roles_accepted
from datetime import datetime

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


@web_service.route("/monitor", methods=["GET"])
@login_required
@roles_accepted("admin")
def monitor():
    """
    Maps monitor path to a static index file
    :return: Rendered template
    """
    return render_template("general/gpio.html",
                           socket_url=WEB_SERVICE_CONFIG["host"],
                           socket_port=WEB_SERVICE_CONFIG["socket_port"])
