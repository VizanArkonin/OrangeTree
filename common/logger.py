import logging


class LogLevel:
    """
    Simple enum to define the logging levels
    NOTE: It is a tiny bit restructured copy of log levels from logging library, taken here for consistency.
    """
    CRITICAL = "critical"
    FATAL = CRITICAL
    ERROR = "error"
    WARNING = "warning"
    WARN = WARNING
    INFO = "info"
    DEBUG = "debug"

    value = {
        CRITICAL: 50,
        ERROR: 40,
        WARNING: 30,
        INFO: 20,
        DEBUG: 10
    }


class Logger:
    """
    Main logger factory. Used to create, instantiate, set and operate the logger instance.
    """
    _logger_format = "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s"

    def __init__(self, name, logging_level=LogLevel.DEBUG):
        logging.basicConfig(format=self._logger_format)

        self._logger = logging.getLogger(name)
        self._logger.setLevel(LogLevel.value.get(logging_level))

    def log(self, level, text):
        """
        Main logger workhorse - used to simplify access to Pin's logger
        :param level: String - level of log message
        :param text: String - message itself
        :return: None
        """
        lvl = str(level).lower()
        if lvl == LogLevel.INFO:
            self._logger.info(text)
        elif lvl == LogLevel.WARNING:
            self._logger.warning(text)
        elif lvl == LogLevel.DEBUG:
            self._logger.debug(text)
        elif lvl == LogLevel.ERROR:
            self._logger.error(text)
        elif lvl == LogLevel.CRITICAL:
            self._logger.critical(text)
        else:
            self._logger.warning(text)
