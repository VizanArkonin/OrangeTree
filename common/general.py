import importlib
import os
import sys


def import_all_modules_from(relative_path_from_main):
    """
    This function goes through all files and folders in given module and imports everything.
    Primarily, it is to be used to import module contents (DB models, Flask routes and so on), that are structured
    within given module
    :param relative_path_from_main: Relative path from work dir root to a target module (i.e. 'web/routes')
    :return: None
    """
    for root, subdirs, files in os.walk(relative_path_from_main):
        for file_name in files:
            if file_name.endswith(".py"):
                if file_name != "__init__.py":
                    # strip the extension
                    module = file_name[:-3]

                    # reformat the path string and import the module

                    if sys.platform.lower() == "linux" or sys.platform.lower() == "posix":
                        # Linux-based formatting
                        importlib.import_module(root.replace("/", ".") + "." + module)
                    elif sys.platform.lower() == "win32" or sys.platform.lower() == "win64":
                        # Windows-based formatting
                        importlib.import_module(root.replace("\\", ".") + "." + module)


def get_formatter():
    """
    Logger format provider
    :return: Format String
    """
    return "%(asctime)s; %(levelname)s; %(message)s"


def get_time_formatter():
    """
    Datetime-to-string conversion format provider
    :return: Format String
    """
    return "%Y-%m-%d %H:%M:%S"
