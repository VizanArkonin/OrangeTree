from flask import request

from flask_login import login_required
from flask_socketio import emit, join_room

from web import socket_service

ROOM = "gpio"


@socket_service.on("join", namespace='/gpio')
@login_required
def join_gpio_room():
    join_room(ROOM)


@socket_service.on('getStatus', namespace='/gpio')
@login_required
def request_status(message):
    """
    Requests current PINs status. Used by both 'connected' and regular events.
    :param message: Socket payload. Should have following structure:

    {
        "justForMe": Boolean
    }

    "justForMe" specifies if it should be emitted to everyone, or just the client who sent a request

    :return: None
    """
    """
    if message["justForMe"]:
        emit('status', gpio_controller.get_pins_status(), room=request.sid)
    else:
        emit('status', gpio_controller.get_pins_status(), room=ROOM)
    """


@socket_service.on("setPinMode", namespace="/gpio")
@login_required
def set_pin_mode(message):
    """
    Sets the specified pin mode and sends the update call to the rest of clients.
    :param message: Socket payload. Should have following structure:

    {
        "pinID": int/str,
        "modeID": int/str
    }

    :return: None
    """
    """
    gpio_controller.get_pin(int(message["pinID"])).set_mode(int(message["modeID"]))

    emit('status', gpio_controller.get_pins_status(), room=ROOM)
    """


@socket_service.on("setOutput", namespace="/gpio")
@login_required
def set_pin_output(message):
    """
    Sets the 1 or 0 for an OUTPUT-mode pin.
    :param message: Socket payload. Should have following structure:

    {
        "pinID": int/str,
        "value": int/str
    }

    :return: None
    """
    """
    gpio_controller.get_pin(int(message["pinID"])).set_output(int(message["value"]))

    emit('status', gpio_controller.get_pins_status(), room=ROOM)
    """


@socket_service.on("setPinLock", namespace="/gpio")
@login_required
def set_pin_lock(message):
    """
    Locks/unlocks the specified pin
    :param message: Socket payload. Should have following structure:

    {
        "pinID": int/str,
        "locked": bool
    }

    :return: None
    """
    """
    if message["locked"]:
        gpio_controller.get_pin(int(message["pinID"])).lock_pin()
    else:
        gpio_controller.get_pin(int(message["pinID"])).unlock_pin()

    emit('status', gpio_controller.get_pins_status(), room=ROOM)
    """
