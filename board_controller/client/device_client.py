import errno
import json
from time import sleep

from gpio import gpio_controller
from board_controller.common.packets.packet_status import PacketStatus
from board_controller.common.socket_connector import SocketConnector
from board_controller.common.packets.general import *
from board_controller.common.packets.gpio import GET_PIN_CONFIGURATION, GET_STATUS


class DeviceClient(SocketConnector):
    """
    Main client workhorse, serves as socket interface to operate incoming and outcoming transmission
    """
    def __init__(self, host, port, device_id, device_type, device_key):
        super().__init__(host, port)
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
            self.log("info", "Socket client - Connecting to {0}:{1}".format(self.host, self.port))
            self.sock.connect((self.host, self.port))
        except ConnectionRefusedError:
            self.log("error", "Could not connect to '{0}:{1}'. Retrying in 2 seconds".format(self.host, self.port))
            sleep(2)
            self.connect()

    def authenticate(self):
        """
        Authentication sequence - sends the AUTH packet, waits for response and validates if it was successful.
        :return:
        """
        auth_packet = AUTH(self.client_id, self.device_type, self.device_key, PacketStatus.REQUESTED.value)
        self.sock.sendall(self.get_cipher().encrypt(json.dumps(auth_packet)))
        res = self.sock.recv(1024)
        if res:
            response = json.loads(self.get_cipher().decrypt(res))
            device_id = response["payload"]["deviceID"]
            status = response["payload"]["status"]

            if device_id == self.client_id and status == PacketStatus.ACCEPTED.value:
                self.log("info", "Authorization request accepted. Proceeding")
            elif device_id == self.client_id and status == PacketStatus.DENIED.value:
                self.log("error", "Authorization denied.")
                for error in response["errors"]:
                    self.log("error", error)
                self.sock.close()
        else:
            self.log("error", "AUTH - Empty response received. Did server close connection?")
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
                    self.log("warning", "Lost connection to server. Trying to re-connect")
                    self.reconnect()
            except OSError as error:
                # This exception handler covers the case when server shuts down with client being connected.
                if error.errno == errno.ECONNRESET:
                    self.log("warning", "Server closed the connection (CONN_RESET). Trying to re-connect")
                    self.reconnect()
                elif error.errno == errno.EBADF:
                    self.log("critical", "Connection was forcibly closed. Shutting down")
                    break

    def process_request(self, data):
        """
        Main packet processing workhorse, that routes calls to respective processor functions.

        :param data: Raw, encrypted byte array
        :return: None
        """
        try:
            decoded_data = self.get_cipher().decrypt(data)
            deserialized_data = json.loads(decoded_data)
            call_name = deserialized_data["call"]
            if call_name in self.client_routes:
                self.client_routes[call_name](self, deserialized_data)
            else:
                self.log("error", "No routes for call '{0}' were found".format(call_name))
        except UnicodeDecodeError as error:
            self.log("error", "Processing error - {0}".format(error))
            self.log("error", "Decoded data - {0}".format(decoded_data))

    def send(self, data):
        """
        Serializes, encrypts and sends given packet dict to a client.

        :param data: Data packet dict
        :return: None
        """
        self.sock.sendall(self.get_cipher().encrypt(json.dumps(data)))

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
        self.log("info", "Resetting pin configuration and requesting new one from the server")
        gpio_controller.reload_pins(reset_pins=True)

        self.send(GET_PIN_CONFIGURATION(self.client_id))
