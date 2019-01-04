"""
Socket server - GPIO board calls routing library.
"""
from common.socket_connector.packets.packet_base import SocketPacket
from common.socket_connector.utils import generic_response_validator
from server.socket_server import __server as server
from server.database.models.device.devices import Devices


@server.route(packet_name="GetGPIOBoardPinConfig")
def pin_config(client, data):
    """
    GPIO Config processor

    :param client: ClientThread instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    device_id = data.payload.deviceId

    if device_id:
        device = Devices.query.filter(Devices.device_id == device_id).first()
        new_payload = {
            "configuration": device.serialize_config()
        }
        new_packet = SocketPacket(call_name=data.call, call_payload=new_payload, errors_list=data.errors)

        client.send(new_packet)


@server.route(packet_name="GetGPIOBoardStatus")
def status(client, data):
    """
    GPIO board status processor.

    :param client: ClientThread instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    errors = data.errors

    client.client_gpio_status = data.payload.status
    if errors:
        client.log("error", "{0} Client - GetGPIOBoardStatus route processing errors:")
        for error in errors:
            client.log("error", error)


@server.route(packet_name="SetGPIOPinMode")
def set_mode(client, data):
    """
    Validates if client GPIO pin mode change was successful

    :param client: ClientThread instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    generic_response_validator(client, data, "SetGPIOPinMode")


@server.route(packet_name="SetGPIOPinOutput")
def set_output(client, data):
    """
    Validates if client GPIO pin output change was successful

    :param client: ClientThread instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    generic_response_validator(client, data, "SetGPIOPinOutput")


@server.route(packet_name="SetGPIOPinLock")
def set_lock(client, data):
    """
    Validates if client GPIO pin lock change was successful

    :param client: ClientThread instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    generic_response_validator(client, data, "SetGPIOPinLock")
