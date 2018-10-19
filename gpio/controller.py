import logging
from datetime import datetime

from gpio.utils import wiringpi_is_used
from gpio.pin import Pin
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


class GpioController:
    """
    Main GPIO board control center.
    Serves as programatical representation of GPIO board, providing access to it's pins and allowing monitoring.
    Note - this class is intended to be a singleton (to prevent data/flow collisions).
    """
    _logger = logging.getLogger("gpio_controller")
    # Since this class is intended to be a singleton, we instantiate static dict for pins
    _PINS = {}

    def __init__(self):
        self._logger.setLevel(logging.DEBUG)
        self._logger.info("Initializing GPIO Controller")
        if wiringpi_is_used():
            import wiringpi
            wiringpi.wiringPiSetup()
        # Since there is a gap between 17 and 20 pins (they do not exist), we use 2 separate for loops for creation
        for pin in range(0, 17):
            self._PINS[pin] = Pin(pin, OUTPUT)
        for pin in range(21, 32):
            self._PINS[pin] = Pin(pin, OUTPUT)

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
