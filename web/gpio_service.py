"""
Routing library for all GPIO-related requests
"""

import json

from gpio import gpio_controller
from web import web_service, utils


@web_service.route("/gpio/status", methods=["GET"])
def get_all_pins_status():
    """
    Requests current status of all GPIO pins on the board
    :return: JSON details string
    """
    return utils.get_response(
        json.dumps(gpio_controller.get_pins_status()),
        "text/json")


@web_service.route("/gpio/status/<int:pin_id>", methods=["GET"])
def get_pin_status(pin_id):
    """
    Requests current status of specified pin
    :param pin_id: Pin ID (parsed by Flask from path)
    :return: JSON details string
    """
    return utils.get_response(
        json.dumps(gpio_controller.get_pin_status(pin_id)),
        "text/json")
