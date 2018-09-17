import logging
from gpio.main import GpioController

logging.basicConfig()
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
logger.info("starting up")

# Singleton initialization area
gpio_controller = GpioController()



