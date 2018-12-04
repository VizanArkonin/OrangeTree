"""
Routing library for all GPIO-related requests
"""
import json

from flask import render_template
from flask_security import login_required, roles_required, roles_accepted

import config
from config import WEB_SERVICE_CONFIG
from board_controller.server import server_interface
from web import web_service, utils
from web.utils import MimeType

# Until Home page and device selection is available, we hard-code it to a single configured client
BOARD_ID = config.CLIENT_CONFIG["device_id"]


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


@web_service.route("/gpio/status", methods=["GET"])
@login_required
@roles_accepted("admin")
def get_all_pins_status():
    """
    Requests current status of all GPIO pins on the board
    :return: JSON details string
    """

    return utils.get_response(
        json.dumps(server_interface.get_board_status(BOARD_ID)),
        mimetype=MimeType.JSON_MIMETYPE.value)


@web_service.route("/gpio/status/<int:pin_id>", methods=["GET"])
@login_required
@roles_accepted("admin")
def get_pin_status(pin_id):
    """
    Requests current status of specified pin
    :param pin_id: Pin ID (parsed by Flask from path)
    :return: JSON details string
    """
    """
    return utils.get_response(
        json.dumps(gpio_controller.get_pin_status(pin_id)),
        mimetype=MimeType.JSON_MIMETYPE.value)
    """
