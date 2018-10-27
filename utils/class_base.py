import logging

from Crypto.Cipher import AES

import config
from utils.general import get_formatter

logging.basicConfig(format=get_formatter())


class ClassBase(object):
    """
    This class serves as inheritance base for every other class that will require universal features, like logger,
    decryptor and such.
    """
    def __init__(self):
        self._logger = logging.getLogger(__class__.__name__)
        self._logger.setLevel(logging.DEBUG)

    def _log(self, level, text):
        """
        Main logger workhorse - used to simplify access to Pin's logger
        :param level: String - level of log message
        :param text: String - message itself
        :return: None
        """
        lvl = str(level).lower()
        if lvl == "info":
            self._logger.info(text)
        elif lvl == "warning":
            self._logger.warning(text)
        elif lvl == "debug":
            self._logger.debug(text)
        elif lvl == "error":
            self._logger.error(text)
        elif lvl == "critical":
            self._logger.critical(text)
        else:
            self._logger.warning(text)

    def get_cipher(self, key=config.BOARD_SERVICE_CONFIG["crypto_key"],
                   initialization_vector=config.BOARD_SERVICE_CONFIG["crypto_iv"]):
        """
        Returns new AES cipher object, used to encrypt and decrypt given strings.

        :param key: String - Cipher Key. For current mode (CFB), it must be 16, 24 or 32 bytes (string characters) long
        (respectively for AES-128, AES-192 or AES-256)
        :param initialization_vector: String - Initialization vector to use for encryption or decryption.
        For current mode (CFB), it MUST be 16 bytes (string characters) long.
        :return: AES Cipher instance
        """
        return AES.new(key, AES.MODE_CFB, initialization_vector)
