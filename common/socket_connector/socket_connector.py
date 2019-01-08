import socket

from common.class_base import ClassBase
from common.logger import LogLevel


class SocketConnector(ClassBase):
    """
    Starter template for socket-based classes. Creates and implements core variables.
    """
    def __init__(self, host, port, logger_name, logging_level):
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.host = host
        self.port = port
        self.client_routes = {}
        self.sock = None
        self.create_socket()
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
        Sets listener anchor to false, shutting loop down.
        :return: None
        """
        self.log(LogLevel.INFO, "Client listener shut down.")
        self.active = False

    def _add_route(self, packet_name, function):
        """
        Adds given function as route processor.

        :param packet_name: Name of packet to route
        :param function: Function to process it
        :return: None
        """
        if packet_name in self.client_routes:
            self.log(LogLevel.WARNING, "Attempt to re-assign route '{0}' blocked".format(packet_name))
        else:
            self.client_routes[packet_name] = function

    def create_socket(self, family=socket.AF_INET, type=socket.SOCK_STREAM):
        """
        Creates a socket object and assigns it to self.sock variable

        :param family: Connection family
        :param type: Connection type
        :return: None
        """
        self.sock = socket.socket(family, type)
