from client.config import GENERAL
from common.logger import Logger, LogLevel

logger = Logger("main", logging_level=GENERAL["logging_level"])
logger.log(LogLevel.INFO, "Starting up")

"""
We mimic the Node-like architecture by separating parts of app into self-contained modules.
Initialization is performed during module import (in __init__.py files).
"""

# Service imports. Used to initialize modules and their respective processes/variables. DO NOT REMOVE THEM!
logger.log(LogLevel.INFO, "Starting GPIO adapter")
import client.gpio
logger.log(LogLevel.INFO, "Starting Device client")
import client.socket_connector
logger.log(LogLevel.INFO, "Starting Device controller module")
import client.board_controller
# End of service imports

logger.log(LogLevel.INFO, "Start-up complete")
