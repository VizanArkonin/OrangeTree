"""
Routes library initialization area.
NOTE: Since this sub-module is intended to be structured storage for Device socket server routes,
we recursively import EVERYTHING that is included in this package.
Restrain from adding any utils or misc functions/classes here to keep namespace clean.
"""
import os

from common.general import import_all_modules_from

import_all_modules_from(os.path.dirname(__file__).replace(os.getcwd(), "")[1:])