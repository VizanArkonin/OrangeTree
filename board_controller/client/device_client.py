import json

from board_controller.common.packets.packet_status import PacketStatus
from board_controller.common.socket_connector import SocketConnector
from board_controller.common.packets.general import *


class DeviceClient(SocketConnector):
    """
    Main client workhorse, serves as socket interface to operate incoming and outcoming transmission
    """
    def __init__(self, host, port, device_id, device_type, device_key):
        super().__init__(host, port)
        self.client_id = device_id
        self.device_type = device_type
        self.device_key = device_key
        self.sock.connect((self.host, self.port))
        self.authenticate()

    def authenticate(self):
        auth_packet = AUTH(self.client_id, self.device_type, self.device_key, PacketStatus.REQUESTED.value)
        self.sock.sendall(self.get_cipher().encrypt(json.dumps(auth_packet)))
        res = self.sock.recv(10240)
        response = json.loads(self.get_cipher().decrypt(res))

        if response["payload"]["deviceID"] == self.client_id \
                and response["payload"]["status"] == PacketStatus.ACCEPTED.value:
            self.log("info", "Authorization request accepted. Proceeding")
        elif response["payload"]["deviceID"] == self.client_id \
                and response["payload"]["status"] == PacketStatus.DENIED.value:
            self.log("error", "Authorization denied.")
            for error in response["errors"]:
                self.log("error", error)

    def listen(self):
        while self.active:
            data = self.sock.recv(10240)
            self.process_request(data)

    def process_request(self, data):
        """
        Main packet processing workhorse, that routes calls to respective processor functions.

        :param data: Raw, encrypted byte array
        :return: None
        """
        decoded_data = self.get_cipher().decrypt(data)
        deserialized_data = json.loads(decoded_data)
        call_name = deserialized_data["call"]
        if call_name in self.client_routes:
            self.client_routes[call_name](self, deserialized_data)
        else:
            self.log("error", "No routes for call '{0}' were found".format(call_name))

    def send(self, data):
        """
        Serializes, encrypts and sends given packet dict to a client.

        :param data: Data packet dict
        :return: None
        """
        self.sock.sendall(self.get_cipher().encrypt(json.dumps(data)))
