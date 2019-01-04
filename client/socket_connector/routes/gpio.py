"""
Socket client - GPIO board calls routing library.
"""
from client.gpio import gpio_controller
from client.socket_connector import socket_client as Client
from common.socket_connector.packets.gpio import *


@Client.route(packet_name="GetGPIOBoardPinConfig")
def pin_config(client, data):
    """
    GPIO board config processor - receives the config from server and stores it in client instance.

    :param client: DeviceClient instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    gpio_controller.set_pin_config(data.payload.configuration)


@Client.route(packet_name="GetGPIOBoardStatus")
def status(client, data):
    """
    GPIO board status processor - gets current board status and sends it in status packet.

    :param client: DeviceClient instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    message = GET_STATUS(status=gpio_controller.get_pins_status())

    client.send(message)


@Client.route(packet_name="SetGPIOPinMode")
def set_mode(client, data):
    """
    Processes pin mode change request. As a response, it sends out updated status packet.

    :param client: DeviceClient instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    try:
        gpio_controller.get_pin(data.payload.pinID).set_mode(data.payload.pinMode)
        client.send(GET_STATUS(status=gpio_controller.get_pins_status()))
    except Exception as exception:
        client.send(GET_STATUS(status=gpio_controller.get_pins_status(), errors=[exception]))


@Client.route(packet_name="SetGPIOPinOutput")
def set_output(client, data):
    """
    Processes pin output value change request. As a response, it sends out updated status packet.

    :param client: DeviceClient instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    try:
        gpio_controller.get_pin(data.payload.pinID).set_output(data.payload.outputValue)
        client.send(GET_STATUS(status=gpio_controller.get_pins_status()))
    except Exception as exception:
        client.send(GET_STATUS(status=gpio_controller.get_pins_status(), errors=[exception]))


@Client.route(packet_name="SetGPIOPinLock")
def set_lock(client, data):
    """
    Processes pin lock change request. As a response, it sends out updated status packet.

    :param client: DeviceClient instance
    :param data: SocketPacket instance with decrypted and deserialized data
    :return: None
    """
    pin_id = data.payload.pinID
    try:
        if data.payload.locked:
            gpio_controller.get_pin(pin_id).lock_pin()
        else:
            gpio_controller.get_pin(pin_id).unlock_pin()
        client.send(GET_STATUS(status=gpio_controller.get_pins_status()))
    except Exception as exception:
        client.send(GET_STATUS(status=gpio_controller.get_pins_status(), errors=[exception]))
