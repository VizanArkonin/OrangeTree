from time import sleep

from common.socket_connector.packets.packet_status import PacketStatus
from common.class_base import ClassBase
import common.socket_connector.packets.gpio as GpioPacket
from server.config import GENERAL


class SocketInterface(ClassBase):
    """
    Interface for interacting with socket server - wrapper for requests composition and validation.
    """
    def __init__(self, server_instance):
        """
        :param server_instance: Instance of SocketServer
        """
        super().__init__(logger_name=__class__.__name__, logging_level=GENERAL["logging_level"])
        self._server = server_instance

    def get_device_pin_config(self, board_id):
        """
        Returns a dict with pin configuration for given board
        :param board_id: Board ID
        :return: Pin configuration dict (or None, if client is not connected/disconnected)
        """
        client = self._server.get_client_by_id(board_id)
        if client:
            if client.is_alive():
                return client.client_pin_config
            else:
                return None
        else:
            return None

    def is_client_alive(self, board_id):
        """
        Checks if given client is present and alive.

        :param board_id: Board ID
        :return: True (connected, alive) or False (disconnected, not yet connected, listener thread is down)
        """
        client = self._server.get_client_by_id(board_id)
        if client:
            if client.is_alive():
                return True
            else:
                return False
        else:
            return False

    def get_device_db_id(self, board_id):
        """
        Checks if provided client exists in DB, and if yes - returns it's row ID.
        NOTE: It uses allowed_devices array to prevent unnecessary DB calls.

        :param board_id: Board ID
        :return: Board ID row ID in database
        """
        return [device.id for device in self._server.allowed_devices if device.device_id == board_id][0]

    def get_board_status(self, board_id):
        """
        Requests GPIO board status from a given board. Once received, it updates client's client_gpio_status container.

        :param board_id: Board ID
        :return: None
        """
        client = self._server.get_client_by_id(board_id)
        if client:
            if not client.client_gpio_status:
                client.send(GpioPacket.GET_STATUS())
                while client.client_gpio_status is None:
                    sleep(0.05)
            return client.client_gpio_status

    def set_pin_mode(self, board_id, pin_id, mode_id):
        """
        Request to change pin mode to a given board.

        :param board_id: Board ID
        :param pin_id: Pin ID
        :param mode_id: Mode ID. See GPIO Controller lib for ID's reference
        :return: None
        """
        client = self._server.get_client_by_id(board_id)
        if client:
            packet = GpioPacket.SET_PIN_MODE(pin_id, mode_id, PacketStatus.REQUESTED.value)
            client.send(packet)

    def set_pin_output(self, board_id, pin_id, value):
        """
        Request to set pin output value to a given board

        :param board_id: Board ID
        :param pin_id: Pin ID
        :param value: Value. Can be 1(ON) or 0 (OFF). Works only for pin in OUTPUT mode.
        :return: None
        """
        client = self._server.get_client_by_id(board_id)
        if client:
            packet = GpioPacket.SET_PIN_OUTPUT(pin_id, value, PacketStatus.REQUESTED.value)
            client.send(packet)

    def set_pin_lock(self, board_id, pin_id, locked):
        """
        Request to lock or unlock pin to a given board

        :param board_id: Board ID
        :param pin_id: Pin ID
        :param locked: Bool - True (lock) or False (unlock)
        :return: None
        """
        client = self._server.get_client_by_id(board_id)
        if client:
            packet = GpioPacket.SET_PIN_LOCK(pin_id, locked, PacketStatus.REQUESTED.value)
            client.send(packet)
