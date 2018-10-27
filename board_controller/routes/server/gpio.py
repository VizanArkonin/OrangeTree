"""
Socket server - GPIO board calls routing library.
"""

from board_controller.server import server


@server.route(packet_name="GetGPIOBoardStatus")
def status(client, data):
    """
    GPIO board status processor. Covers both incoming and outcoming calls

    :param client: ClientThread instance
    :param data: Serialized and encrypted data byte array
    :return: None
    """
    response = data

