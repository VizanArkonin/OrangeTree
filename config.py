"""
Core configuration file
"""

# DB section
DATABASE_CONFIG = {
    "connection_string": "sqlite:///database.db",
    "autocommit": False,
    "autoflush": False
}

# Flask (web-service) section
WEB_SERVICE_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": False,
    "security_secret_key": "super-secret",
    "security_password_hash": "bcrypt",
    "security_password_salt": "$2a$06$6sSyl34Zw.48NBXwGBSURO",
    "session_timeout_in_minutes": 10,
    "static_url_path": "",
    "static_files_path": "../static",
    "templates_path": "../templates"
}
