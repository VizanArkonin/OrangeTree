from flask import request

from flask_login import login_required
from flask_socketio import emit, join_room

import config
from board_controller.server import server_interface

from web import socket_service

ROOM = "gpio"

BOARD_ID = config.CLIENT_CONFIG["device_id"]


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
    if message["justForMe"]:
        emit('status', server_interface.get_board_status(BOARD_ID), room=request.sid)
    else:
        emit('status', server_interface.get_board_status(BOARD_ID), room=ROOM)


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
    pin_id = int(message["pinID"])
    mode = int(message["modeID"])
    server_interface.set_pin_mode(BOARD_ID, pin_id, mode)

    emit('status', server_interface.get_board_status(BOARD_ID), room=ROOM)


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
    pin_id = int(message["pinID"])
    value = int(message["value"])
    server_interface.set_pin_output(BOARD_ID, pin_id, value)

    emit('status', server_interface.get_board_status(BOARD_ID), room=ROOM)


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
    pin_id = int(message["pinID"])
    locked = bool(message["locked"])
    server_interface.set_pin_lock(BOARD_ID, pin_id, locked)

    emit('status', server_interface.get_board_status(BOARD_ID), room=ROOM)
