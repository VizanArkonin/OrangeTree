"""
Socket client.
Provides low-level connection interface for Orange PI board connection. 1 Instance of socket server is run on host
and 1 Instance of client is run on single given board.
"""
from threading import Thread

import config
from board_controller.client.device_client import DeviceClient

# First, we create SocketServer instance
client = DeviceClient(config.BOARD_SERVICE_CONFIG["host"], config.BOARD_SERVICE_CONFIG["port"],
                      config.CLIENT_CONFIG["device_id"], config.CLIENT_CONFIG["device_type"],
                      config.CLIENT_CONFIG["device_key"])

# Then we import everything from respective routing library. DO NOT REMOVE THIS IMPORT!
import board_controller.routes.client


def listen():
    """
    Payload for server thread - keep listener up while being run from inside the thread.
    :return: None
    """
    try:
        client.listen()
    except KeyboardInterrupt:
        client.shut_down()


# Finally, we initiate the server thread and start it
client_thread = Thread(target=listen)
client_thread.start()
