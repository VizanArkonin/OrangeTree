"""
GPIO service packets library.
Contains all packets, used to control GPIO board, called by both server and client.
To ease data forming, all packets are stored as functions, which allows generating them on fly just by passing data in.
NOTE: All method names are in upper case for reading clarity
"""


def GET_STATUS(status={}, errors=[]):
    """
    Packet for GPIO board status request. Payload contains the dict with status on all pins.

    :param status: Dict with pins status. Server sends it as empty dict, client response pulls data from
    GPIO controller's get_pins_status() method.
    :param errors: Error strings list.
    :return: Packet dict.
    """
    return {
        "call": "GetGPIOBoardStatus",
        "payload":
            {
                "status": status
            },
        "errors":
            errors
    }


def SET_PIN_MODE(pin_id, mode_id, status, errors=[]):
    """
    Pin status change packet.

    :param pin_id: GPIO board pin number.
    :param mode_id: Mode ID. See GPIO Controller class for reference.
    :param status: Request status. Can be "requested", "success" or "failed" (see PacketStatus enum for reference)
    :param errors: Error strings list.
    :return: Packet dict.
    """
    return {
        "call": "SetGPIOPinMode",
        "payload":
            {
                "pinID": int(pin_id),
                "pinMode": int(mode_id),
                "status": status
            },
        "errors":
            errors
    }


def SET_PIN_OUTPUT(pin_id, value, status, errors=[]):
    """
    Pin output value change packet.

    :param pin_id: GPIO board pin number.
    :param value: Value. Can be 0 (OFF) or 1 (ON)
    :param status: Request status. Can be "requested", "success" or "failed" (see PacketStatus enum for reference)
    :param errors: Error strings list.
    :return: Packet dict.
    """
    return {
        "call": "SetGPIOPinOutput",
        "payload":
            {
                "pinID": int(pin_id),
                "outputValue": int(value),
                "status": status
            },
        "errors":
            errors
    }


def SET_PIN_LOCK(pin_id, value, status, errors=[]):
    """
    Pin lock change packet.

    :param pin_id: GPIO board pin number.
    :param value: Value. Can be True or False (bool)
    :param status: Request status. Can be "requested", "success" or "failed" (see PacketStatus enum for reference)
    :param errors: Error strings list.
    :return: Packet dict.
    """
    return {
        "call": "SetGPIOPinLock",
        "payload":
            {
                "pinID": int(pin_id),
                "locked": bool(value),
                "status": status
            },
        "errors":
            errors
    }