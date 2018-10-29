import json
import logging
import socket
from json import JSONDecodeError
from time import sleep

from board_controller.common.packets.packet_status import PacketStatus
from board_controller.common.socket_connector import SocketConnector
from board_controller.common.packets import general as Packets
from board_controller.server.client_thread import ClientThread
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
                            device_id = deserialized_data["payload"]["deviceID"]
                            response_packet = Packets.AUTH(device_id,
                                                           deserialized_data["payload"]["deviceType"],
                                                           deserialized_data["payload"]["key"],
                                                           PacketStatus.DENIED.value,
                                                           ["Device is not allowed in the system"])
                            client.sendall(self.get_cipher().encrypt(json.dumps(response_packet)))
                            client.close()
                            self.log("warning", "Client '{0} {1}' is not allowed. Rejecting auth and closing client".
                                     format(deserialized_data["payload"]["deviceID"], address))
                    else:
                        self.log("warning", "Invalid authorization packet received from {0}. Disconnecting".
                                 format(address))
                        client.close()
                except JSONDecodeError:
                    self.log("warning", "Couldn't deserialize request. Format is incorrect. Message was - {0}".
                             format(decoded_data))
                    client.close()

    def get_client_by_id(self, client_id):
        """
        Returns client instance by given device ID.
        :param client_id: Device ID
        :return: ClientThread instance (or none, if client doesn't exist)
        """
        try:
            client = self.clients[client_id]
            if client.is_alive():
                return client
            else:
                self.log("error", "Client with ID '{0}' got disconnected.".format(client_id))
                return None
        except KeyError:
            self.log("error", "Client with ID '{0}' is not connected yet.".format(client_id))
            return None

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
        self._logger.info("Authorization for '{0} {1}' has passed. Client registered.".format(device_id, address))
        client.sendall(self.get_cipher().encrypt(json.dumps(Packets.AUTH(device_id,
                                                                         request_data["payload"]["deviceType"],
                                                                         request_data["payload"]["key"],
                                                                         PacketStatus.ACCEPTED.value))))
