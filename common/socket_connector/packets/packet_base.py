import json
from collections import namedtuple


class SocketPacket(object):
    """
    Base class for socket service packets. Serves as a serializable interface to generate, serialize, deserialize and
    process socket packet messages.
    """
    def __init__(self, call_name="", call_payload={}, errors_list=[]):
        """
        :param call_name: (String) Call name. Optional (default value - empty string).
        :param call_payload: (Dict) Payload information. Optional (default value - empty dict).
        :param errors_list: (List) List of error strings, if any. Optional (default value - empty list).
        """
        self.call = call_name
        self.payload = self.__generate_payload(call_payload)
        self.errors = errors_list

    def serialize(self):
        """
        Serializes object into JSON-friendly dict
        :return: Packet Dict
        """
        return {
            "call": self.call,
            "payload": dict(self.payload._asdict()),
            "errors": self.errors
        }

    def deserialize(self, packet):
        """
        Extracts provided dict values (or transforms packet string into a dict first) and sets respective attributes.
        :return: SocketPacket instance (self)
        """
        if type(packet) is str:
            # First case - packet is string. It means we need to transform it into a dict first.
            deserialized_packet = json.loads(packet)
        elif type(packet) is dict:
            # If it's already a dict - we simply proceed.
            deserialized_packet = packet
        else:
            raise Exception("Failed to deserialize packet. It must be either String or Dict")

        self.call = deserialized_packet["call"]
        self.payload = self.__generate_payload(deserialized_packet["payload"])
        self.errors = deserialized_packet["errors"]

        return self

    def __generate_payload(self, payload_dict):
        """
        Generates named tuple for a payload dict.

        :param payload_dict: Payload Dict.
        :return: Payload namedtuple
        """
        Payload = namedtuple("Payload", sorted(payload_dict))
        return Payload(**payload_dict)
