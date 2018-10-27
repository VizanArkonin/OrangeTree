"""
General packets library.
Contains all general-use packets, used by both server and client.
To ease data forming, all packets are stored as functions, which allows generating them on fly just by passing data in.
NOTE: All method names are in upper case for reading clarity
"""


def AUTH(device_id, device_type, status, errors=[]):
    """
    Core authorization packet.

    :param device_id: Device ID. Refers to device_id column of devices_list table.
    :param device_type: Device Type ID. Refers to type_id column of device_types table.
    :param status: Response status. Can be "requested", "accepted" or "denied"
    :param errors: Error strings list.
    :return: Packet dict
    """
    return {
        "call": "Authorize",
        "payload":
            {
                "deviceID": device_id,
                "deviceType": device_type,
                "status": status
            },
        "errors":
            errors
    }



