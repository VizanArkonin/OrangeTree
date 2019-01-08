from common.logger import Logger, LogLevel
from server.config import GENERAL

logger = Logger("main", logging_level=GENERAL["logging_level"])
logger.log(LogLevel.INFO, "Starting up")

"""
We mimic the Node-like architecture by separating parts of app into self-contained modules.
Initialization is performed during module import (in __init__.py files).
"""

# Service imports. Used to initialize modules and their respective processes/variables. DO NOT REMOVE THEM!
logger.log(LogLevel.INFO, "Starting Web and Database service")
import server.web
logger.log(LogLevel.INFO, "Starting Device server")
import server.socket_server
# End of service imports

logger.log(LogLevel.INFO, "Start-up complete")
