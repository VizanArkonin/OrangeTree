import config


def wiringpi_is_used():
    """
    Some debugging/development tasks don't require wiringpi library. To prevent constant commenting and
    disabling, we use this validator - it checks respective config flag - whether we use it or not.
    :return: Boolean
    """
    return config.WEB_SERVICE_CONFIG["use_wiringpi"]