import logging
from datetime import datetime
from threading import Thread
from time import sleep

from client.gpio.utils import live_mode_is_on
from client.gpio.pin import Pin
from common.class_base import ClassBase
from common.general import get_formatter

logging.basicConfig(format=get_formatter())

# Copied from wiringpi root
# Pin modes
INPUT = 0
OUTPUT = 1
PWM_OUTPUT = 2
GPIO_CLOCK = 3
SOFT_PWM_OUTPUT = 4
SOFT_TONE_OUTPUT = 5
PWM_TONE_OUTPUT = 6

LOW = 0
HIGH = 1


class GpioController(ClassBase):
    """
    Main GPIO board control center.
    Serves as programatical representation of GPIO board, providing access to it's pins and allowing monitoring.
    NOTE - this class is intended to be a singleton (to prevent data/flow collisions).
    """
    # Since this class is intended to be a singleton, we instantiate static dict for pins
    _PINS = {}

    def __init__(self):
        super().__init__()
        self.log("info", "Initializing GPIO Controller")
        if live_mode_is_on():
            import wiringpi
            wiringpi.wiringPiSetup()
        self._pins_config = None

    def set_pin_config(self, config):
        """
        Setter for pins config. Used from socket client controller as interface method -
        direct approach causes circular dependency
        :param config: Config dict
        :return: None
        """
        self._pins_config = config

    def load_pins(self):
        """
        Reads the pins config and initializes respective wPi pins.
        NOTE: We run waiter in threaded mode to prevent process locks.
        :return: None
        """
        self.log("info", "Waiting for pin configuration")
        while not self._pins_config:
            sleep(1)

        self.log("info", "Pin configuration received. Initializing pin controllers")
        for pin in self._pins_config["pins"]:
            if pin["type"] == "wPi":
                pin_wpi = pin["wPi"]
                self._PINS[pin_wpi] = Pin(pin_wpi, OUTPUT)

    def reload_pins(self, reset_pins=False):
        """
        Resets the state of all currently initialized pins, retrieves fresh config and re-initializes pin controllers.

        :param reset_pins: Pin config variable reset trigger
        :return: None
        """
        # First, we reset existing pins to OUTPUT-OFF state
        for key, value in self._PINS.items():
            value.unlock_pin()
            value.set_mode(OUTPUT)
            value.set_output(0)

        # Then, we re-initialize pins storage and config, retrieve the new data and re-initialize pins
        if reset_pins:
            self._pins_config = None
        self._PINS = {}
        Thread(target=self.load_pins).start()

    def get_pin(self, pinNo):
        return self._PINS[pinNo]

    def get_all_pins(self):
        return self._PINS

    def get_pins_status(self):
        """
        Collects statuses from individual pins and composes a JSON-like dict with current values
        :return: Dict with status values
        """
        pins_list = []

        for key, pin in self.get_all_pins().items():
            pins_list.append(pin.get_pin_status())

        return {"timestamp": datetime.now().isoformat(),
                "pins_status": pins_list}

    def get_pin_status(self, pin_id):
        """
        Check on given pin and returns a JSON-like dict with it's current state
        :param pin_id: Pin ID
        :return: Dict with status values
        """
        return {"timestamp": datetime.now().isoformat(),
                "pin_status": self.get_pin(pin_id).get_pin_status()}
