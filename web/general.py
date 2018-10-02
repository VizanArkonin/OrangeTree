"""
General routing library
"""

from flask_security import login_required, roles_required, roles_accepted

from web import web_service


@web_service.route("/monitor", methods=["GET"])
@login_required
@roles_accepted("admin")
def monitor():
    """
    Maps monitor path to a static index file
    :return: Static file
    """
    return web_service.send_static_file("index.html")
