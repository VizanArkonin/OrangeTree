import types

from threading import Thread
from time import sleep
import logging

from gpio.utils import wiringpi_is_used
from utils.general import get_formatter

logging.basicConfig(format=get_formatter())

if wiringpi_is_used():
    import wiringpi


def default_callback(pin_instance):
    """
    Default callback, used for both HIGH and LOW input states if no other callbacks specified
    :return: None
    """
    logger = logging.getLogger("GPIO_PIN_{0}".format(pin_instance.get_pin()))
    logger.setLevel(logging.DEBUG)
    logger.debug("Default callback triggered")


class Pin:
    """
    Operational interface for GPIO pins, represents a given PIN on the plate.
    Uses simple lockable API to prevent same pin being used by multiple objects/threads at the same time
    """
    _pin = None                 # Int
    _mode = None                # Int (0 to 6, )
    _state = None               # Int (1 or 0)
    _locked = None              # Boolean

    _input_monitor = None       # Thread
    _input_control = None       # Thread

    _logger = None              # Logger instance
    _low_callback = None        # Tuple (function, *args)
    _high_callback = None       # Tuple (function, *args)
    _reset_callbacks = None     # Boolean

    def __init__(self, pin, mode):
        """
        :param pin: wPi pin number
        :param mode: operational mode (ranges from 0 to 6, see wiringpi modes)
        """
        self._logger = logging.getLogger("GPIO_PIN_{0}".format(pin))
        self._logger.setLevel(logging.DEBUG)
        self.__log("info", "Initializing {0} GPIO Pin controller with {1} mode".format(pin, mode))
        self._pin = pin
        self._mode = mode
        if wiringpi_is_used():
            wiringpi.pinMode(pin, mode)
            self._state = wiringpi.digitalRead(pin)
        else:
            self._state = 0
        self.set_low_callback(default_callback, self)
        self.set_high_callback(default_callback, self)
        self._reset_callbacks = False
        self._locked = False

    def get_pin(self):
        return self._pin

    def get_mode(self):
        return self._mode

    def get_state(self):
        return self._state

    def get_pin_status(self):
        """
        Generates and returns dict with pin status (pin. mode, state, lock)
        :return: Dict with status values
        """
        return {
            "pin": self._pin,
            "mode": self._mode,
            "state": self._state,
            "locked": self._locked
        }

    """
    Locking pin forbids a number of procedures from running. 
    This is done to safeguard current pin state and prevent mode/value collisions
    """

    def lock_pin(self):
        self._locked = True
        self.__log("info", "Pin locked")

        return self

    def unlock_pin(self):
        self._locked = False
        self.__log("info", "Pin unlocked")

        return self

    def set_mode(self, mode):
        """
        Switches/sets pin mode to selected value. See main controller for Pin modes
        :param mode: Pin mode ID
        :return: None
        """
        if not self._locked:
            self._mode = mode
            if wiringpi_is_used():
                wiringpi.pinMode(self._pin, mode)
            if mode == 0:
                self.__start_input_monitor()
                self.lock_pin()
            else:
                if self._reset_callbacks:
                    self.perform_callbacks_reset()

            self.__log("info", "Mode set to {0}".format(mode))
        else:
            self.__log("warning", "Attempt to change mode of a locked pin. Unlock it first")

        return self

    def set_output(self, state):
        """
        Sets the OUTPUT pin value to either LOW (0) or HIGH (1). Works ONLY in OUTPUT mode
        :param state: State ID (1 or 0)
        :return: None
        """
        if not self._locked:
            if self._mode == 1:
                self.__log("info", "Setting output to {0}".format(state))

                if wiringpi_is_used():
                    wiringpi.digitalWrite(self._pin, state)
                self._state = state
            else:
                self.__log("warning", "Set Output is only available for PIN working in OUTPUT mode")
        else:
            self.__lock_access_warning()
        return self

    """
    Callbacks are functions that's being executed when INPUT-mode pin changes it's state.
    Low callback is run when state changes from 1 to 0. High callback is run when state changes from 0 to 1
    As soon as PIN is switched to INPUT mode, threaded state monitor is launched. When it detects a state change,
    it launches a respective callback method. 
    Functions are also run in separate thread to prevent monitor from hanging during callback execution.
    When you switch PIN out of INPUT mode, you can make it reset both callbacks to default function. To do that,
    you must call reset_callbacks(True) method (By default it is False)
    """

    def set_low_callback(self, fun, *args):
        if isinstance(fun, types.FunctionType):
            self._low_callback = (fun, args)
            self.__log("info", "Low callback was set")
        else:
            self.__log("warning", "Callback must be a function. Did you remove () from the end of the name?")

    def set_high_callback(self, fun, *args):
        if isinstance(fun, types.FunctionType):
            self._high_callback = (fun, args)
            self.__log("info", "High callback was set")
        else:
            self.__log("warning", "Callback must be a function. Did you remove () from the end of the name?")

    def reset_callbacks(self, true_or_false):
        self._reset_callbacks = bool(true_or_false)

    def perform_callbacks_reset(self):
        self.set_low_callback(default_callback, self)
        self.set_high_callback(default_callback, self)
        self.__log("info", "Default callbacks were set")

    """
    Private service methods
    """

    def __input_monitor(self):
        """
        Thread payload, that listens to state change of the input pin.
        :return: None
        """
        while self._mode == 0:
            if wiringpi_is_used():
                new_state = wiringpi.digitalRead(self._pin)
            else:
                if self._state == 0:
                    new_state = 1
                else:
                    new_state = 0

            if self._state != new_state:
                self.__log("info", "Input state change detected. Was {0}, now {1}".
                           format(self._state, new_state))
                self._state = new_state
                if new_state == 0:
                    self._input_control = Thread(target=self._low_callback[0], args=self._low_callback[1])
                elif new_state == 1:
                    self._input_control = Thread(target=self._high_callback[0], args=self._high_callback[1])
                self._input_control.setDaemon(True)
                self._input_control.start()

            sleep(0.05)

    def __start_input_monitor(self):
        """
        Method creates and starts s pin listening thread
        :return: None
        """
        self.__log("info", "Starting input monitor")
        self._input_monitor = Thread(target=self.__input_monitor)
        self._input_monitor.setDaemon(True)
        self._input_monitor.start()

    def __log(self, level, text):
        """
        Main logger workhorse - used to simplify access to Pin's logger
        :param level: String - level of log message
        :param text: String - message itself
        :return: None
        """
        start = "PIN-{0} - ".format(self._pin) if self._pin != None else ""
        lvl = str(level).lower()
        if lvl == "info":
            self._logger.info("{0}{1}".format(start, text))
        elif lvl == "warning":
            self._logger.warning("{0}{1}".format(start, text))
        elif lvl == "debug":
            self._logger.debug("{0}{1}".format(start, text))
        elif lvl == "error":
            self._logger.error("{0}{1}".format(start, text))
        elif lvl == "critical":
            self._logger.critical("{0}{1}".format(start, text))
        else:
            self._logger.warning("{0}invalid logging level specified".format(start))

    def __lock_access_warning(self):
        """
        Throws a logger warning when user attempts to use locked pin
        :return: None
        """
        self.__log("info", "Attempt to change output value for locked pin. Unlock it first")
