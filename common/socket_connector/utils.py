"""
Utility functions and variables
"""
from common.socket_connector.packets.packet_status import PacketStatus


def generic_response_validator(client, data, route_name):
    """
    Generic response validator, defines standard response success validation logic.

    :param client: Client instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :param route_name: Route name
    :return: None
    """
    status = data.payload.status
    errors = data.errors
    if status == PacketStatus.SUCCESS.value:
        return
    elif status == PacketStatus.FAILED.value:
        if errors:
            client.log("error", "{0} Client - {1} route processing errors:".format(client.client_id, route_name))
            for error in errors:
                client.log("error", error)
            return
    else:
        client.log("error", "{0} Client - Unknown status response: {0}".format(status))
