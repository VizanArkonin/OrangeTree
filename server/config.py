"""
Core configuration file - Server side
"""
from common.logger import LogLevel

# General section
GENERAL = {
    "logging_level": LogLevel.DEBUG
}

# DB section
DATABASE_CONFIG = {
    # Connection string pattern - {connection_type}://{user}:{password}@{host}:{port}/{database name}
    # SQLite3 connection string - "sqlite:///../database/database.db?check_same_thread=False"
    "connection_string": "mysql+mysqlconnector://root:@127.0.0.1:3306/hephaestus",
    "autocommit": False,
    "autoflush": True
}

# Flask (web-service) section
WEB_SERVICE_CONFIG = {
    "host": "127.0.0.1",
    "web_port": 5000,
    "socket_port": 5001,
    "debug": False,
    "use_wiringpi": False,
    "security_secret_key": "super-secret",
    "security_password_hash": "bcrypt",
    "security_password_salt": "$2a$06$6sSyl34Zw.48NBXwGBSURO",
    "session_timeout_in_minutes": 10,
    "refresh_session_on_each_request": True,
    "static_url_path": "",
    "static_files_path": "../static",
    "templates_path": "../templates"
}

# Board socket service section
BOARD_SERVICE_CONFIG = {
    "host": "127.0.0.1",
    "port": 5002,
    "crypto_key": "SOME_AWESOME_ENCRYPT_KEY",
    "crypto_iv": "SOME_AWESOMEE_IV"
}
