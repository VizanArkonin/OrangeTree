"""
Board Controller service packets library.
Contains all packets, used to transmit system data and control device itself.
To ease data forming, all packets are stored as functions, which allows generating them on fly just by passing data in.
NOTE: All method names are in upper case for reading clarity
"""
from common.socket_connector.packets.packet_base import SocketPacket


def DEVICE_STATUS(device_id, device_status, errors=[]):
    """
    Packet, used to transmit device status to a server.
    NOTE: Device status dict should have the following format:
    {
        "cpuTemperature": Int,
        "cpuLoadPercentage": Int,
        "totalRam": Int,
        "ramUsed": Int,
        "usedRamPercentage": Float
    }

    :param device_id: Device ID. Refers to device_id column in devices_list table.
    :param device_status: Dict with system values.
    :param errors: Error strings list.
    :return: SocketPacket instance.
    """
    payload = {
                "deviceId": device_id,
                "deviceStatus": device_status
              }

    return SocketPacket("DeviceStatus", payload, errors)

