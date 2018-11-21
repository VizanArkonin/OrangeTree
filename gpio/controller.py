import logging
from datetime import datetime

from gpio.utils import wiringpi_is_used
from gpio.pin import Pin
from gpio.boards import *
from utils.class_base import ClassBase
from utils.general import get_formatter

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

    def __init__(self, device_type_id):
        super().__init__()
        self.log("info", "Initializing GPIO Controller")
        if wiringpi_is_used():
            import wiringpi
            wiringpi.wiringPiSetup()
        self.load_pins(device_type_id)

    def load_pins(self, device_type_id):
        if device_type_id == 1:
            for pin in ORANGE_PI_LITE["pins"]:
                if pin["type"] == "wPi":
                    pin_wpi = pin["wPi"]
                    self._PINS[pin_wpi] = Pin(pin_wpi, OUTPUT)

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
