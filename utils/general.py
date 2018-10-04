import importlib
import os


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
                    importlib.import_module(root.replace("/", ".") + "." + module)
