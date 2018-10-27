import json
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
        self.listener_thread = Thread(target=self._listen_to_client)
        self.listener_thread.setDaemon(True)
        self.listener_thread.start()

    def process_request(self, data):
        """
        Main packet processing workhorse, that routes calls to respective processor functions.

        :param data: Decrypted and deserialized message packet.
        :return: None
        """
        decoded_data = self.get_cipher().decrypt(data)
        deserialized_data = json.loads(decoded_data)
        call_name = deserialized_data["call"]
        if call_name in self.routes:
            self.routes[call_name](self, data)
        else:
            self._log("error", "No routes for call '{0}' were found".format(call_name))

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
                data = self.client.recv(1024)
                if data:
                    self.process_request(data)
                else:
                    self._log("info", "Client '{0}' disconnected".format(self.address))
                    break
            except Exception as exception:
                self._log("error","Caught exception: '{0}'\nClosing client '{1}'".format(exception, self.client_id))
                self.client.close()
                return False
