"""
General routing library
"""

from web import web_service


@web_service.route("/", methods=["GET"])
def index():
    """
    Maps root path to a static index file
    :return: Static file
    """
    return web_service.send_static_file("index.html")
