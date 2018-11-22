"""
Socket client - GPIO board calls routing library.
"""
from gpio import gpio_controller
from board_controller.client import client as Client
from board_controller.common.packets.gpio import *


@Client.route(packet_name="GetGPIOBoardPinConfig")
def pin_config(client, data):
    """
    GPIO board config processor - receives the config from server and stores it in client instance.

    :param client: DeviceClient instance
    :param data: Serialized and encrypted data byte array
    :return: None
    """
    gpio_controller.set_pin_config(data["payload"]["configuration"])


@Client.route(packet_name="GetGPIOBoardStatus")
def status(client, data):
    """
    GPIO board status processor - gets current board status and sends it in status packet.

    :param client: DeviceClient instance
    :param data: Serialized and encrypted data byte array
    :return: None
    """
    message = GET_STATUS(status=gpio_controller.get_pins_status())

    client.send(message)


@Client.route(packet_name="SetGPIOPinMode")
def set_mode(client, data):
    """
    Processes pin mode change request. As a response, it sends out updated status packet.

    :param client: DeviceClient instance
    :param data: Decrypted and deserialized packet dict
    :return: None
    """
    pin_id = data["payload"]["pinID"]
    pin_mode = data["payload"]["pinMode"]
    try:
        gpio_controller.get_pin(pin_id).set_mode(pin_mode)
        client.send(GET_STATUS(status=gpio_controller.get_pins_status()))
    except Exception as exception:
        client.send(GET_STATUS(status=gpio_controller.get_pins_status(), errors=[exception]))


@Client.route(packet_name="SetGPIOPinOutput")
def set_output(client, data):
    """
    Processes pin output value change request. As a response, it sends out updated status packet.

    :param client: DeviceClient instance
    :param data: Decrypted and deserialized packet dict
    :return: None
    """
    pin_id = data["payload"]["pinID"]
    value = data["payload"]["outputValue"]
    try:
        gpio_controller.get_pin(pin_id).set_output(value)
        client.send(GET_STATUS(status=gpio_controller.get_pins_status()))
    except Exception as exception:
        client.send(GET_STATUS(status=gpio_controller.get_pins_status(), errors=[exception]))


@Client.route(packet_name="SetGPIOPinLock")
def set_lock(client, data):
    """
    Processes pin lock change request. As a response, it sends out updated status packet.

    :param client: DeviceClient instance
    :param data: Decrypted and deserialized packet dict
    :return: None
    """
    pin_id = data["payload"]["pinID"]
    locked = data["payload"]["locked"]
    try:
        if locked:
            gpio_controller.get_pin(pin_id).lock_pin()
        else:
            gpio_controller.get_pin(pin_id).unlock_pin()
        client.send(GET_STATUS(status=gpio_controller.get_pins_status()))
    except Exception as exception:
        client.send(GET_STATUS(status=gpio_controller.get_pins_status(), errors=[exception]))
