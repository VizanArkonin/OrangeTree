import logging
from gpio.main import GpioController
from time import sleep

from utils.log_formatter import get_formatter

logging.basicConfig(format=get_formatter())
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
logger.info("Starting up")

# Singleton initialization area
gpio_controller = GpioController()
