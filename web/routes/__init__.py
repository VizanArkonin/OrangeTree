"""
Routes library initialization area
NOTE: Due to initialization nature, we can't contain it in module's __all__ list, so we import them here, one by one.
"""
from . import general
from . import gpio_service
