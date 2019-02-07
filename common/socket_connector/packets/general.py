"""
General packets library.
Contains all general-use packets, used by both server and client.
To ease data forming, all packets are stored as functions, which allows generating them on fly just by passing data in.
NOTE: All method names are in upper case for reading clarity
"""
from common.socket_connector.packets.packet_base import SocketPacket


def AUTH(device_id="", device_type="", key="", status="", errors=[]):
    """
    Core authorization packet.

    :param device_id: Device ID. Refers to device_id column in devices_list table.
    :param device_type: Device Type ID. Refers to type_id column in device_types table.
    :param key: Device key. Refers to key column in devices_list_table
    :param status: Response status. Can be "requested", "accepted" or "denied" (see PacketStatus enum for reference)
    :param errors: Error strings list.
    :return: SocketPacket instance.
    """
    payload = {
                "deviceId": device_id,
                "deviceType": device_type,
                "key": key,
                "status": status
              }

    return SocketPacket("Authorize", payload, errors)



