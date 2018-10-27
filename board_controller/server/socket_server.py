import json
import logging
import socket
from json import JSONDecodeError

from board_controller.common.socket_connector import SocketConnector
from board_controller.server.client_interface import ClientThread
from board_controller.common.packets import general as Packets
from database.models.device import DevicesList
from utils.general import get_formatter

logging.basicConfig(format=get_formatter())


class SocketServer(SocketConnector):
    """
    Device Socket Server.
    Serves as main gateway for incoming client transmissions, validating if they're allowed and generating respective
    client representation objects.
    """
    def __init__(self, host, port):
        super().__init__(host, port)
        self.clients = {}
        self.client_routes = {}
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.allowed_devices = DevicesList.query.all()

    def listen(self):
        """
        Listens for new connections, validates if they're allowed and puts them in clients list.
        :return: None
        """
        self.sock.listen(5)
        while self.active:
            client, address = self.sock.accept()
            self._logger.info("Accepted new connection from '{0}'. Waiting for authorization packet".format(address))
            data = client.recv(1024)
            if data:
                try:
                    decoded_data = self.get_cipher().decrypt(data)
                    deserialized_data = json.loads(decoded_data)
                    if deserialized_data["call"] == "Authorize":
                        if self._device_is_allowed(deserialized_data):
                            self._accept_and_add_client(client, address, deserialized_data)
                        else:
                            response_packet = Packets.AUTH(deserialized_data["payload"]["deviceID"],
                                                           deserialized_data["payload"]["deviceType"],
                                                           "denied",
                                                           ["Device is not allowed in the system"])
                            client.sendall(self.get_cipher().encrypt(json.dumps(response_packet)))
                            client.close()
                            self._log("warning", "Client '{0}' is not allowed. Rejecting auth and closing client".
                                      format(address))
                    else:
                        self._log("warning","Invalid authorization packet received from {0}. Disconnecting".
                                  format(address))
                        client.close()
                except JSONDecodeError:
                    self._log("warning","Couldn't deserialize request. Format is incorrect. Message was - {0}".
                              format(decoded_data))
                    client.close()

    def shut_down(self):
        """
        Sets listener anchor to false, shutting listener loop down.
        :return: None
        """
        self._log("info", "Client listener shut down.")
        self.active = False

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

    def _add_route(self, packet_name, function):
        """
        Adds given function as route processor.

        :param packet_name: Name of packet to route
        :param function: Function to process it
        :return: None
        """
        if packet_name in self.client_routes:
            self._logger.warning("Attempt to re-assign route '{0}' blocked".format(packet_name))
        else:
            self.client_routes[packet_name] = function

    def _device_is_allowed(self, data):
        """
        Goes through list of allowed devices and validates if requested device is in it.

        :param data: Decrypted and deserialized request packet.
        :return: Boolean
        """
        return any(device for device in self.allowed_devices if
                   device.device_id == data["payload"]["deviceID"] and
                   device.device_type == int(data["payload"]["deviceType"]) and
                   device.device_access_key == data["payload"]["key"])

    def _accept_and_add_client(self, client, address, request_data):
        """
        Creates client handler, adds it to clients list and sends confirmation package back to sender

        :param client: Socket client instance
        :param address: Socket address tuple
        :param request_data: Decrypted and deserialized request packet.
        :return: None
        """
        device_id = request_data["payload"]["deviceID"]
        client_handler = ClientThread(client, address, device_id)
        client_handler.routes = self.client_routes
        self.clients[device_id] = client_handler
        self._logger.info("Authorization for '{0}' has passed. Client registered.".format(address))
        client.sendall(self.get_cipher().encrypt(json.dumps(Packets.AUTH(device_id,
                                                                         request_data["payload"]["deviceType"],
                                                                         "accepted"))))
