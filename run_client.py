import logging

from common.general import get_formatter

logging.basicConfig(format=get_formatter())
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
logger.info("Starting up")

"""
We mimic the Node-like architecture by separating parts of app into self-contained modules.
Initialization is performed during module import (in __init__.py files).
"""

# Service imports. Used to initialize modules and their respective processes/variables. DO NOT REMOVE THEM!
logger.info("Starting GPIO adapter")
import client.gpio
logger.info("Starting Device client")
import client.socket_connector
logger.info("Starting Device controller module")
import client.board_controller
# End of service imports

logger.info("Start-up complete")
