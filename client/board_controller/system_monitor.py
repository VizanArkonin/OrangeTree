from time import sleep

from common.class_base import ClassBase
from common.logger import LogLevel
from common.socket_connector.packets.board_controller import DEVICE_STATUS
from client.socket_connector import socket_client
from client.config import CLIENT_CONFIG, GENERAL
from client.gpio.utils import live_mode_is_on
from random import randint, getrandbits
import psutil


class SystemMonitor(ClassBase):
    """
    Thread service, used to monitor device state and periodically send the status message to server.
    """
    def __init__(self):
        super().__init__(logger_name=__class__.__name__, logging_level=GENERAL["logging_level"])
        self.cpu_temperature = 0
        self.cpu_load_percentage = 0
        self.total_ram = 0
        self.ram_used = 0
        self.used_ram_percentage = 0

    def run(self):
        """
        Main thread workhorse - runs on timer, and when it hits - updates the values and sends the update packet.
        :return: None
        """
        while True:
            try:
                self.update_values()
                self.send_status()
            except KeyboardInterrupt:
                self.log(LogLevel.INFO, "Caught Interrupt signal. Stopping system monitor thread")
                return
            except Exception as exception:
                self.log(LogLevel.ERROR, "Caught exception - {0}".format(exception))
            finally:
                sleep(CLIENT_CONFIG["status_update_tick_in_seconds"])

    def update_values(self):
        """
        Reads current system values (or randomizes the values, if client is in demo mode) and updates the value conts.
        :return: None
        """
        if live_mode_is_on():
            try:
                # Orange PI devices running armbian have the temperature available from "iio_hwmon" kernel library.
                self.cpu_temperature = psutil.sensors_temperatures()["iio_hwmon"][0].current
            except KeyError:
                # If that key is not present - we assume that temp sensors are not available.
                self.cpu_temperature = 0

            self.cpu_load_percentage = psutil.cpu_percent(interval=5)

            memory_readings = psutil.virtual_memory()
            self.total_ram = round(memory_readings.total / 1000)
            self.ram_used = round(memory_readings.used / 1000)
            self.used_ram_percentage = memory_readings.percent

        else:
            # If we're in demo mode, we simulate the board by invoking pseudo-random values generation.
            # To provide values consistency, we check if it is 0, and if not - we increment/decrement the previous value
            self.cpu_temperature = randint(35, 57) \
                if self.cpu_temperature == 0 \
                else self.__get_altered_value(self.cpu_temperature, 35, 57, randint(1, 4))
            self.cpu_load_percentage = randint(5, 30) \
                if self.cpu_load_percentage == 0 \
                else self.__get_altered_value(self.cpu_load_percentage, 5, 30, randint(1, 3))
            self.total_ram = 512000
            self.ram_used = randint(56000, 92000) \
                if self.ram_used == 0 \
                else self.__get_altered_value(self.ram_used, 56000, 92000, randint(64, 4068))

        self.used_ram_percentage = round((self.ram_used / (self.total_ram / 100)), 2)

    def send_status(self):
        """
        Pulls current system values, puts them in a dict packet and send it to server.
        :return: None
        """
        packet = DEVICE_STATUS(CLIENT_CONFIG["device_id"], self.__get_status())
        socket_client.send(packet)

    def __get_status(self):
        """
        Packs current values in a dict and returns it
        :return: Status dict
        """
        return {
            "cpuTemperature": self.cpu_temperature,
            "cpuLoadPercentage": self.cpu_load_percentage,
            "totalRam": self.total_ram,
            "ramUsed": self.ram_used,
            "usedRamPercentage": self.used_ram_percentage
        }

    def __get_altered_value(self, initial_value, low_border, high_border, step):
        """
        Method, used solely by demo mode - used to alter the existing value.

        :param initial_value: Initial parameter value
        :param low_border: Lowest value border
        :param high_border: Highest value border
        :param step: Forward/backward value change step
        :return: (Int) New value
        """
        # We use random boolean trigger to determine whether we will increment or decrement
        if not getrandbits(1):
            if (initial_value + step) > high_border:
                return initial_value - step
            else:
                return initial_value + step
        else:
            if (initial_value - step) < low_border:
                return initial_value + step
            else:
                return initial_value - step
