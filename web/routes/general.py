"""
General routing library
"""

from flask import render_template
from flask_security import login_required, roles_required, roles_accepted

from web import web_service


@web_service.route("/monitor", methods=["GET"])
@login_required
@roles_accepted("admin")
def monitor():
    """
    Maps monitor path to a static index file
    :return: Rendered template
    """
    return render_template("general/gpio.html")
