"""
Socket server - general calls routing library.
"""

from server.socket_server import __server as server


@server.route(packet_name="Echo")
def echo(client, data):
    """
    Basic Echo-test route. Used to validate client connectivity without triggering any system changes.

    :param client: ClientThread instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    response = data
    client.send(response)
