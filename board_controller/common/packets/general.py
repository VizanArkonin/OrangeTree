"""
General packets library.
Contains all general-use packets, used by both server and client.
To ease data forming, all packets are stored as functions, which allows generating them on fly just by passing data in.
NOTE: All method names are in upper case for reading clarity
"""


def AUTH(device_id, device_type, key, status, errors=[]):
    """
    Core authorization packet.

    :param device_id: Device ID. Refers to device_id column of devices_list table.
    :param device_type: Device Type ID. Refers to type_id column of device_types table.
    :param key: Device key. Refers to key column of devices_list_table
    :param status: Response status. Can be "requested", "accepted" or "denied" (see PacketStatus enum for reference)
    :param errors: Error strings list.
    :return: Packet dict
    """
    return {
        "call": "Authorize",
        "payload":
            {
                "deviceID": device_id,
                "deviceType": device_type,
                "key": key,
                "status": status
            },
        "errors":
            errors
    }



