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
        self.client_routes = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active = True

    def route(self, packet_name):
        """
        Routing decorator.
        Used for methods that will map certain packet types to their respective processors.
        NOTE: All methods using this decorator MUST accept 2 arguments - client (Client instance) and data (decrypted,
        deserialized request).
        Example - def echo(client, data):

        :param packet_name: Name of packet to route
        :return: Decorator function
        """
        def decorator(f):
            self._add_route(packet_name, f)
            return f
        return decorator

    def shut_down(self):
        """
        Sets listener anchor to false, shutting listener loop down.
        :return: None
        """
        self.log("info", "Client listener shut down.")
        self.active = False

    def _add_route(self, packet_name, function):
        """
        Adds given function as route processor.

        :param packet_name: Name of packet to route
        :param function: Function to process it
        :return: None
        """
        if packet_name in self.client_routes:
            self.log("warning", "Attempt to re-assign route '{0}' blocked".format(packet_name))
        else:
            self.client_routes[packet_name] = function

