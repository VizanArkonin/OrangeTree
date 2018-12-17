"""
Socket client.
Provides low-level connection interface for Orange PI boards. 1 Instance of socket server is run on host
and 1 Instance of client is run on single given board.
"""
from threading import Thread

import client.config as config
from client.socket_connector.device_client import DeviceClient

# First, we create DeviceClient instance
socket_client = DeviceClient(config.BOARD_SERVICE_CONFIG["host"], config.BOARD_SERVICE_CONFIG["port"],
                             config.CLIENT_CONFIG["device_id"], config.CLIENT_CONFIG["device_type"],
                             config.CLIENT_CONFIG["device_key"])

# Then we import everything from respective routing library. DO NOT REMOVE THIS IMPORT!
import client.socket_connector.routes


def listen():
    """
    Payload for server thread - keep listener up while being run from inside the thread.
    :return: None
    """
    try:
        socket_client.listen()
    except KeyboardInterrupt:
        socket_client.shut_down()


# Finally, we initiate the client thread and start it
client_thread = Thread(target=listen)
client_thread.start()
