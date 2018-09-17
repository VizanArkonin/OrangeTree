import wiringpi
import logging
from gpio.pin import Pin

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
    _logger = logging.getLogger("gpio_controller")
    _PINS = {}

    def __init__(self):
        self._logger.info("Initializing GPIO Controller")
        wiringpi.wiringPiSetup()
        # Since there is a gap between 17 and 20 pins (they do not exist), we use 2 separate for loops for creation
        for pin in range(0, 17):
            self._PINS[pin] = Pin(pin, OUTPUT)
        for pin in range(21, 32):
            self._PINS[pin] = Pin(pin, OUTPUT)

    def get_pin(self, pinNo):
        return self._PINS[pinNo]
