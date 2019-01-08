import errno
import json
from time import sleep

from client.config import GENERAL
from client.gpio import gpio_controller
from common.logger import LogLevel
from common.socket_connector.packets.packet_status import PacketStatus
from common.socket_connector.socket_connector import SocketConnector
from common.socket_connector.packets.general import *
from common.socket_connector.packets.gpio import GET_PIN_CONFIGURATION


class DeviceClient(SocketConnector):
    """
    Main client workhorse, serves as socket interface to operate incoming and outcoming transmission
    """
    def __init__(self, host, port, device_id, device_type, device_key):
        super().__init__(host, port, logger_name=__class__.__name__, logging_level=GENERAL["logging_level"])
        self.client_id = device_id
        self.device_type = device_type
        self.device_key = device_key
        self.connect()
        self.authenticate()
        self.request_pin_configuration()

    def connect(self):
        """
        Connection loop - attempts to connect to the server, retrying each 2 seconds if connection is being refused.
        :return: None
        """
        try:
            self.log(LogLevel.INFO, "Socket client - Connecting to {0}:{1}".format(self.host, self.port))
            self.sock.connect((self.host, self.port))
        except ConnectionRefusedError:
            self.log(LogLevel.ERROR, "Could not connect to '{0}:{1}'. Retrying in 2 seconds".format(self.host, self.port))
            sleep(2)
            self.connect()

    def authenticate(self):
        """
        Authentication sequence - sends the AUTH packet, waits for response and validates if it was successful.
        :return:
        """
        auth_packet = AUTH(self.client_id, self.device_type, self.device_key, PacketStatus.REQUESTED.value)
        self.sock.sendall(self.get_cipher().encrypt(json.dumps(auth_packet.serialize())))
        res = self.sock.recv(1024)
        if res:
            response = SocketPacket().deserialize(self.get_cipher().decrypt(res))
            device_id = response.payload.deviceId
            status = response.payload.status

            if device_id == self.client_id and status == PacketStatus.ACCEPTED.value:
                self.log(LogLevel.INFO, "Authorization request accepted. Proceeding")
            elif device_id == self.client_id and status == PacketStatus.DENIED.value:
                self.log(LogLevel.ERROR, "Authorization denied.")
                for error in response["errors"]:
                    self.log(LogLevel.ERROR, error)
                self.sock.close()
        else:
            self.log(LogLevel.ERROR, "AUTH - Empty response received. Did server close connection?")
            self.sock.close()

    def listen(self):
        """
        Listens to incoming transmission, handles data processing and exceptions handling.
        :return: None
        """
        while self.active:
            try:
                data = self.sock.recv(10240)
                if data:
                    self.process_request(data)
                else:
                    self.log(LogLevel.WARNING, "Lost connection to server. Trying to re-connect")
                    self.reconnect()
            except OSError as error:
                # This exception handler covers the case when server shuts down with client being connected.
                if error.errno == errno.ECONNRESET:
                    self.log(LogLevel.WARNING, "Server closed the connection (CONN_RESET). Trying to re-connect")
                    self.reconnect()
                elif error.errno == errno.EBADF:
                    self.log(LogLevel.CRITICAL, "Connection was forcibly closed. Shutting down")
                    break

    def process_request(self, data):
        """
        Main packet processing workhorse, that routes calls to respective processor functions.

        :param data: Raw, encrypted byte array
        :return: None
        """
        try:
            decoded_data = self.get_cipher().decrypt(data)
            request = SocketPacket().deserialize(decoded_data)
            call_name = request.call
            if call_name in self.client_routes:
                self.client_routes[call_name](self, request)
            else:
                self.log(LogLevel.ERROR, "No routes for call '{0}' were found".format(call_name))
        except UnicodeDecodeError as error:
            self.log(LogLevel.ERROR, "Processing error - {0}".format(error))
            self.log(LogLevel.ERROR, "Decoded data - {0}".format(decoded_data))

    def send(self, data):
        """
        Serializes, encrypts and sends given packet dict to a client.

        :param data: Data packet dict
        :return: None
        """
        try:
            self.sock.sendall(self.get_cipher().encrypt(json.dumps(data.serialize())))
        except BrokenPipeError:
            self.log(LogLevel.ERROR, "[BrokenPipeError] Attempted to send a message through a closed client.")

    def reconnect(self):
        """
        Closes existing socket, creates and opens a new one, connects and performs authentication.
        :return: None
        """
        self.sock.close()
        self.create_socket()
        self.connect()
        self.authenticate()
        self.request_pin_configuration()

    def request_pin_configuration(self):
        """
        Resets and requests pin configuration from the server
        :return: None
        """
        self.log(LogLevel.INFO, "Resetting pin configuration and requesting new one from the server")
        gpio_controller.reload_pins(reset_pins=True)

        self.send(GET_PIN_CONFIGURATION(self.client_id))
