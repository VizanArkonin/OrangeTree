import json
import socket
from datetime import datetime
from json import JSONDecodeError

from common.logger import LogLevel
from common.socket_connector.packets.general import AUTH
from common.socket_connector.packets.packet_base import SocketPacket
from common.socket_connector.packets.packet_status import PacketStatus
from common.socket_connector.socket_connector import SocketConnector
from common.socket_connector.packets import general as Packets
from server.config import GENERAL
from server.socket_server.client_thread import ClientThread
from server.web import db as database
from server.database.models.device.devices import Devices


class SocketServer(SocketConnector):
    """
    Device Socket Server.
    Serves as main gateway for incoming client transmissions, validating if they're allowed and generating respective
    client representation objects.
    """

    def __init__(self, host, port):
        super().__init__(host, port, logger_name=__class__.__name__, logging_level=GENERAL["logging_level"])
        self.clients = {}
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.allowed_devices = Devices.query.all()

    def listen(self):
        """
        Listens for new connections, validates if they're allowed and puts them in clients list.
        :return: None
        """
        self.sock.listen()
        while self.active:
            client, address = self.sock.accept()
            self.log(LogLevel.INFO, "Accepted new connection from '{0}'. Waiting for authorization packet".
                     format(address))
            data = client.recv(1024)
            if data:
                try:
                    decoded_data = self.get_cipher().decrypt(data)
                    request = SocketPacket().deserialize(decoded_data)
                    if request.call == AUTH().call:
                        if self._device_is_allowed(request):
                            self._accept_and_add_client(client, address, request)
                        else:
                            device_id = request.payload.deviceId
                            response_packet = Packets.AUTH(device_id,
                                                           request.payload.deviceType,
                                                           request.payload.key,
                                                           PacketStatus.DENIED.value,
                                                           ["Device is not allowed in the system"])
                            client.sendall(self.get_cipher().encrypt(json.dumps(response_packet)))
                            client.close()
                            self.log(LogLevel.WARNING,
                                     "Client '{0} {1}' is not allowed. Rejecting auth and closing client"
                                     .format(request.payload.deviceId, address))
                    else:
                        self.log(LogLevel.WARNING, "Invalid authorization packet received from {0}. Disconnecting".
                                 format(address))
                        client.close()
                except JSONDecodeError:
                    self.log(LogLevel.WARNING, "Couldn't deserialize request. Format is incorrect. Message was - {0}".
                             format(decoded_data))
                    client.close()

    def get_client_by_id(self, client_id):
        """
        Returns client instance by given device ID.
        :param client_id: Device ID
        :return: ClientThread instance (or None, if client doesn't exist)
        """
        try:
            client = self.clients[client_id]
            if client.is_alive():
                return client
            else:
                self.log(LogLevel.ERROR, "Client with ID '{0}' got disconnected.".format(client_id))
                return None
        except KeyError:
            self.log(LogLevel.ERROR, "Client with ID '{0}' is not connected yet.".format(client_id))
            return None

    def _device_is_allowed(self, data):
        """
        Goes through list of allowed devices and validates if requested device is in it.

        :param data: SocketPacket instance with decrypted and deserialized data
        :return: Boolean
        """
        return any(device for device in self.allowed_devices if
                   device.device_id == data.payload.deviceId and
                   device.device_type_id == int(data.payload.deviceType) and
                   device.device_access_key == data.payload.key)

    def _accept_and_add_client(self, client, address, request_data):
        """
        Creates client handler, adds it to clients list and sends confirmation package back to sender

        :param client: Socket client instance
        :param address: Socket address tuple
        :param request_data: SocketPacket instance with decrypted and deserialized data.
        :return: None
        """
        device_id = request_data.payload.deviceId
        if not self.get_client_by_id(device_id):
            self.log(LogLevel.INFO,
                     "No active clients found for device with ID '{0}'. Initializing new client controller".
                     format(device_id))
            device = Devices.query.filter(Devices.device_id == device_id).first()
            client_handler = ClientThread(client, address, device_id, device.serialize_config())
            client_handler.routes = self.client_routes
            self.clients[device_id] = client_handler
            self.log(LogLevel.INFO, "Authorization for '{0} {1}' has passed. Client registered.".
                     format(device_id, address))
            client_handler.send(Packets.AUTH(device_id,
                                             request_data.payload.deviceType,
                                             request_data.payload.key,
                                             PacketStatus.ACCEPTED.value))

            device.last_address = "{0}:{1}".format(address[0], address[1])
            device.last_connected_at = datetime.now()

            database.session.commit()
        else:
            self.log(LogLevel.ERROR, "Active client with ID '{0}' already registered. Rejecting connection".
                     format(device_id))
            client.close()

    def get_device_by_id(self, id):
        """
        Returns a DevicesList instance for device with given table ID (Or None, if this device is not in the list)

        :param id: Row ID
        :return: DevicesList instance (or None)
        """
        return next((device for device in self.allowed_devices if device.id == id), None)

    def get_device_by_device_id(self, device_id):
        """
        Returns a DevicesList instance for device with given device ID (or None, if this device is not in the list)

        :param device_id: Device ID
        :return: DevicesList instance (or None)
        """
        return next((device for device in self.allowed_devices if device.device_id.lower() == device_id.lower()), None)

    def update_allowed_devices(self):
        """
        Updates the list of allowed devices

        :return: None
        """
        self.allowed_devices = Devices.query.all()
