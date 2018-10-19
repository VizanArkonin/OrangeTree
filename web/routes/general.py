"""
General routing library
"""

from flask import render_template
from flask_security import login_required, roles_required, roles_accepted

from config import WEB_SERVICE_CONFIG
from web import web_service


@web_service.route("/monitor", methods=["GET"])
@login_required
@roles_accepted("admin")
def monitor():
    """
    Maps monitor path to a static index file
    :return: Rendered template
    """
    return render_template("general/gpio.html",
                           socket_url="127.0.0.1" if WEB_SERVICE_CONFIG["host"] == "0.0.0.0"
                                                  else WEB_SERVICE_CONFIG["host"],
                           socket_port=WEB_SERVICE_CONFIG["socket_port"])
