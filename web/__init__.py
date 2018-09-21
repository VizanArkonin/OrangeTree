"""
Web service module.
Provides the REST API layer for interacting with application and it's sub-modules.
Uses Flask micro-framework as main workhorse.
"""
# First, we initialize Flask application itself
from flask import Flask

web_service = Flask(__name__, static_url_path='', static_folder="../static")

# Then we need to import all modules with routes
import web.general
import web.gpio_service

# Once done, we run the web service
web_service.run(host="0.0.0.0")
