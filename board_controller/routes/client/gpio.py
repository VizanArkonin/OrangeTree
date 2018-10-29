"""
Socket client - GPIO board calls routing library.
"""
from gpio import gpio_controller
from board_controller.client import client
from board_controller.common.packets.gpio import *


@client.route(packet_name="GetGPIOBoardStatus")
def status(client, data):
    """
    GPIO board status processor. Covers both incoming and outcoming calls

    :param client: DeviceClient instance
    :param data: Serialized and encrypted data byte array
    :return: None
    """
    message = GET_STATUS(status=gpio_controller.get_pins_status())

    client.send(message)


@client.route(packet_name="SetGPIOPinMode")
def set_mode(client, data):
    """
    Validates if client GPIO pin mode change was successful

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


@client.route(packet_name="SetGPIOPinOutput")
def set_output(client, data):
    """
    Validates if client GPIO pin output change was successful

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


@client.route(packet_name="SetGPIOPinLock")
def set_lock(client, data):
    """
    Validates if client GPIO pin output change was successful

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
