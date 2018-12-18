"""
Board Controller service packets library.
Contains all packets, used to transmit system data and control device itself.
To ease data forming, all packets are stored as functions, which allows generating them on fly just by passing data in.
NOTE: All method names are in upper case for reading clarity
"""


def DEVICE_STATUS(device_id, device_status, errors=[]):
    """
    Core authorization packet.
    NOTE: Device status dict should have the following format:
    {
        "cpuTemperature": Int,
        "cpuLoadPercentage": Int,
        "totalRam": Int,
        "ramUsed": Int,
        "clientStartTime": String (formatted datetime)
    }

    :param device_id: Device ID. Refers to device_id column in devices_list table.
    :param device_status: Dict with system values.
    :param errors: Error strings list.
    :return: Packet dict
    """
    return {
        "call": "DeviceStatus",
        "payload":
            {
                "deviceID": device_id,
                "deviceStatus": device_status
            },
        "errors":
            errors
    }
