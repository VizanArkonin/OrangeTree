import json
from json import JSONDecodeError
from threading import Thread

from utils.class_base import ClassBase


class ClientThread(ClassBase):
    """
    Client handler interface - created and assigned after client have passed authentication.
    Inner thread listens to incoming messages and routes them to respective processor functions.
    """
    def __init__(self, client, address, device_id):
        super().__init__()
        self.client = client
        self.routes = {}
        self.address = address
        self.client_id = device_id
        self.client_gpio_status = {}
        self.listener_thread = Thread(target=self._listen_to_client)
        self.listener_thread.setDaemon(True)
        self.listener_thread.start()

    def process_request(self, data):
        """
        Main packet processing workhorse, that routes calls to respective processor functions.

        :param data: Raw, encrypted byte array
        :return: None
        """
        decoded_data = self.get_cipher().decrypt(data)
        try:
            deserialized_data = json.loads(decoded_data)
            call_name = deserialized_data["call"]
            if call_name in self.routes:
                self.routes[call_name](self, deserialized_data)
            else:
                self.log("error", "No routes for call '{0}' were found".format(call_name))
        except JSONDecodeError as error:
            self.log("error", "Failed to process request. Raw data - {0}".format(decoded_data))

    def send(self, data):
        """
        Serializes, encrypts and sends given packet dict to a client.

        :param data: Data packet dict
        :return: None
        """
        self.client.sendall(self.get_cipher().encrypt(json.dumps(data)))

    def is_alive(self):
        """
        Validates if listener thread is still alive.
        :return: Boolean
        """
        return self.listener_thread.isAlive()

    def _listen_to_client(self):
        """
        Inner thread payload - continuously listens to incoming transmissions, passing them to request processor.
        :return: None
        """
        while True:
            try:
                data = self.client.recv(10240)
                if data:
                    self.process_request(data)
                else:
                    self.log("info", "Client '{0}' disconnected".format(self.address))
                    break
            except Exception as exception:
                self.log("error", "Caught exception: '{0}'\nClosing client '{1}'".format(exception, self.client_id))
                self.client.close()
                return False
