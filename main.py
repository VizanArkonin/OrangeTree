import logging
from time import sleep
from utils.log_formatter import get_formatter

logging.basicConfig(format=get_formatter())
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
logger.info("Starting up")

# Service imports. Used to initialize modules and their respective processes/variables. DO NOT REMOVE THEM!
import web
import gpio
# End of service imports



