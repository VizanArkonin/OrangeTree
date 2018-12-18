import client.config as config


def live_mode_is_on():
    """
    Some debugging/development tasks don't require wiringpi library and some Armbian functionality.
    To prevent constant commenting and disabling, we use this validator - it checks respective config flag -
    whether we use it or not.
    :return: Boolean
    """
    return config.CLIENT_CONFIG["live_mode"]
