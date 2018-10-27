from board_controller.common.packets.packet_status import PacketStatus
from utils.class_base import ClassBase
import board_controller.common.packets.gpio as GpioPacket


class SocketInterface(ClassBase):
    """
    Interface for interacting with socket server - wrapper for requests composition and validation.
    """
    def __init__(self, server_instance):
        """
        :param server_instance: Instance of SocketServer
        """
        super().__init__()
        self._server = server_instance

    def get_board_status(self, board_id):
        client = self._server.get_client_by_id(board_id)
        packet = GpioPacket.GET_STATUS()
        client.send(packet)

        return client.client_gpio_status

    def set_pin_mode(self, board_id, pin_id, mode_id):
        client = self._server.get_client_by_id(board_id)
        packet = GpioPacket.SET_PIN_MODE(pin_id, mode_id, PacketStatus.REQUESTED.value)
        client.send(packet)

    def set_pin_output(self, board_id, pin_id, value):
        client = self._server.get_client_by_id(board_id)
        packet = GpioPacket.SET_PIN_OUTPUT(pin_id, value, PacketStatus.REQUESTED.value)
        client.send(packet)

    def set_pin_lock(self, board_id, pin_id, locked):
        client = self._server.get_client_by_id(board_id)
        packet = GpioPacket.SET_PIN_LOCK(pin_id, locked, PacketStatus.REQUESTED.value)
        client.send(packet)