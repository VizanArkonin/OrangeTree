import logging

from utils.general import get_formatter

logging.basicConfig(format=get_formatter())
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
logger.info("Starting up")

"""
We mimic the Node-like architecture by separating parts of app into self-contained modules.
Initialization is performed during module import (in __init__.py files).
"""

logger.info("Device client")
import board_controller.client
# End of service imports


logger.info("Start-up complete")
