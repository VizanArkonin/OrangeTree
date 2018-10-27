"""
GPIO service packets library.
Contains all packets, used to control GPIO board, called by both server and client.
To ease data forming, all packets are stored as functions, which allows generating them on fly just by passing data in.
NOTE: All method names are in upper case for reading clarity
"""


def GET_STATUS(device_id, status={}, errors=[]):
    """
    Packet for GPIO board status request. Payload contains the dict with status on all pins.

    :param device_id: Device ID. Refers to device_id column of devices_list table.
    :param status: Dict with pins status. Client request sends it as empty dict, server response pulls data from
    GPIO controller's get_pins_status() method.
    :param errors: Error strings list.
    :return: Packet dict.
    """
    return {
        "call": "GetGPIOBoardStatus",
        "payload":
            {
                "deviceID": device_id,
                "status": status
            },
        "errors":
            errors
    }


def SET_PIN_MODE(device_id, pin_id, mode_id, status, errors=[]):
    """
    Pin status change packet.

    :param device_id: Device ID. Refers to device_id column of devices_list table.
    :param pin_id: GPIO board pin number.
    :param mode_id: Mode ID. See GPIO Controller class for reference.
    :param status: Request status. Can be "requested", "success" or "failed"
    :param errors: Error strings list.
    :return: Packet dict.
    """
    return {
        "call": "SetGPIOPinMode",
        "payload":
            {
                "deviceID": device_id,
                "pinID": pin_id,
                "pinMode": mode_id,
                "status": status
            },
        "errors":
            errors
    }


def SET_PIN_OUTPUT(device_id, pin_id, value, status, errors=[]):
    """
    Pin output value change packet.

    :param device_id: Device ID. Refers to device_id column of devices_list table.
    :param pin_id: GPIO board pin number.
    :param value: Value. Can be 0 (OFF) or 1 (ON)
    :param status: Request status. Can be "requested", "success" or "failed"
    :param errors: Error strings list.
    :return: Packet dict.
    """
    return {
        "call": "SetGPIOPinOutput",
        "payload":
            {
                "deviceID": device_id,
                "pinID": pin_id,
                "outputValue": value,
                "status": status
            },
        "errors":
            errors
    }


def SET_PIN_LOCK(device_id, pin_id, value, status, errors=[]):
    """
    Pin lock change packet.

    :param device_id: Device ID. Refers to device_id column of devices_list table.
    :param pin_id: GPIO board pin number.
    :param value: Value. Can be True or False (bool)
    :param status: Request status. Can be "requested", "success" or "failed"
    :param errors: Error strings list.
    :return: Packet dict.
    """
    return {
        "call": "SetGPIOPinLock",
        "payload":
            {
                "deviceID": device_id,
                "pinID": pin_id,
                "locked": value,
                "status": status
            },
        "errors":
            errors
    }