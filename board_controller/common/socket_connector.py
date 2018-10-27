import logging
import socket

from utils.class_base import ClassBase


class SocketConnector(ClassBase):
    """
    Starter template for socket-based classes. Creates and implements core variables.
    """
    def __init__(self, host, port):
        super().__init__()
        self._logger = logging.getLogger(__class__.__name__)
        self._logger.setLevel(logging.DEBUG)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active = True
