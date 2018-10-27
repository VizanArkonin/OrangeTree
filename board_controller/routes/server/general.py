"""
Socket server - general calls routing library.
"""

from board_controller.server import server


@server.route(packet_name="Echo")
def echo(client, data):
    """
    Basic Echo-test route. Used to validate client connectivity without triggering any system changes.

    :param client: ClientThread instance
    :param data: Serialized and encrypted data byte array
    :return: None
    """
    response = data
    client.client.send(response)
    print("Sent '{0}' response to {1}".format(data, client.address))
