"""
Core configuration file - Client side
"""

# Board socket service section
BOARD_SERVICE_CONFIG = {
    "host": "127.0.0.1",
    "port": 5002,
    "crypto_key": "SOME_AWESOME_ENCRYPT_KEY",
    "crypto_iv": "SOME_AWESOMEE_IV"
}

# Client socket service section
# NOTE: Client uses both BOARD_SERVICE and CLIENT_CONFIG dicts, so make sure to update both
CLIENT_CONFIG = {
    "device_id": "DEV_LITE",
    "device_type": 1,
    "device_key": "a3c2061260084f779aa5a7174ce19cd8",
    "live_mode": False
}
