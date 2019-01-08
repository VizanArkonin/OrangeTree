"""
Core configuration file - Client side
"""

# General section
from common.logger import LogLevel

GENERAL = {
    "logging_level": LogLevel.DEBUG
}

# Board socket service section
BOARD_SERVICE_CONFIG = {
    "host": "127.0.0.1",
    "port": 5002,
    "crypto_key": "SOME_AWESOME_ENCRYPT_KEY",
    "crypto_iv": "SOME_AWESOMEE_IV"
}

"""
Client socket service section
NOTE: Client uses BOARD_SERVICE and CLIENT_CONFIG dicts, so make sure to update both

Live Mode defines if client should use the real services a device can provide, or simulate it's behaviour if client is
not run on actual device.
Live mode means:
- Device will use wiringpi library to control real GPIO pins (Demo mode uses wrapper objects only)
- Device will attempt to use services, provided by Armbian (Demo mode will simulate this behaviour)
"""
CLIENT_CONFIG = {
    "device_id": "DEV_LITE",
    "device_type": 1,
    "device_key": "a3c2061260084f779aa5a7174ce19cd8",
    "status_update_tick_in_seconds": 60,
    "live_mode": False
}
