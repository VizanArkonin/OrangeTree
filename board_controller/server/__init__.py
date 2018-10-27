"""
Socket server.
Provides low-level connection interface for Orange PI boards connection. 1 Instance of socket server is run on host
and 1 Instance of client is run on single given board.
Server has it's own authentication system, data packets structure and uses AES encryption.
"""
from threading import Thread

import config
from board_controller.server.socket_server import SocketServer

# First, we create SocketServer instance
server = SocketServer(config.BOARD_SERVICE_CONFIG["host"], config.BOARD_SERVICE_CONFIG["port"])

# Then we import everything from respective routing library. DO NOT REMOVE THIS IMPORT!
import board_controller.routes.server


def listen():
    """
    Payload for server thread - keep listener up while being run from inside the thread.
    :return: None
    """
    try:
        server.listen()
    except KeyboardInterrupt:
        server.shut_down()


# Finally, we initiate the server thread and start it
server_thread = Thread(target=listen)
server_thread.start()
