import wiringpi
from threading import Thread
from time import sleep
import logging
logging.basicConfig()


def default_callback(pin_instance):
    """
    Default callback, used for both HIGH and LOW input states if no other callbacks specified
    :param pin_instance: Instance of Pin object
    :return:
    """
    pin_instance.get_logger().info("PIN-{0} - Input state change detected".format(pin_instance.get_pin()))


class Pin:
    """
    Operational interface for GPIO pins.
    Uses simple lockable API to prevent same pin being used by multiple objects/threads at the same time
    """
    _pin = None             # Int
    _mode = None            # Int (0 to 6, )
    _state = None           # Int (1 or 0)
    _locked = None          # Boolean

    _input_monitor = None   # Thread
    _input_control = None   # Thread

    _logger = None          # Logger instance

    def __init__(self, pin, mode):
        """
        :param pin: wPi pin number
        :param mode: operational mode (ranges from 0 to 6, see wiringpi modes)
        """
        self._logger = logging.getLogger("GPIO_PIN_{0}".format(pin))
        self._logger.setLevel(logging.DEBUG)
        self._logger.info("Initializing {0} GPIO Pin controller with {1} mode".format(pin, mode))
        self._pin = pin
        self._mode = mode
        wiringpi.pinMode(pin, mode)
        self._state = wiringpi.digitalRead(pin)
        self._locked = False

    def lock_pin(self):
        self._locked = True

        return self

    def unlock_pin(self):
        self._locked = False

        return self

    def get_pin(self):
        return self._pin

    def get_mode(self):
        return self._mode

    def get_state(self):
        return self._state

    def get_logger(self):
        return self._logger

    def set_mode(self, mode):
        if not self._locked:
            self._mode = mode
            if mode == 0:
                self.__start_input_monitor(self)
                self.lock_pin()
                self._logger.info("PIN-{0} - mode set to {1}. Input monitor is enabled. Pin locked".
                                  format(self._pin, mode))

        return self

    def set_state(self, state):
        self._state = state

    def set_output_state(self, state):
        if not self._locked:
            if self._mode == 1:
                self._logger.info("PIN-{0} - setting output to {1}".format(self._pin, state))

                wiringpi.digitalWrite(self._pin, state)
                self._state = state
        else:
            self.__lock_access_warning()
        return self

    # Private service methods

    def __input_monitor(self, low_callback=default_callback, high_callback=default_callback, *args):
        """
        Thread payload, that listens to state change of the input pin.
        :return: None
        """
        while self._mode == 0:
            new_state = wiringpi.digitalRead(self._pin)

            if self._state != new_state:
                self._logger.info("PIN-{0} - Input state change detected. Was {1}, now {2}".
                                  format(self._pin, self._state, new_state))
                self._state = new_state
                if new_state == 0:
                    self._input_control = Thread(target=low_callback, args=args)
                elif new_state == 1:
                    self._input_control = Thread(target=high_callback, args=args)
                self._input_control.setDaemon(True)
                self._input_control.start()

            sleep(0.05)

    def __start_input_monitor(self, *args):
        """
        Method creates and starts s pin listening thread
        :return: None
        """
        self._input_monitor = Thread(target=self.__input_monitor(), args=args)
        self._input_monitor.setDaemon(True)
        self._input_monitor.start()

    def __lock_access_warning(self):
        """
        Throws a logger warning when user attempts to use locked pin
        :return: None
        """
        self._logger.warning("PIN-{0} - attempt to change output value for locked pin. Unlock it first".
                             format(self._pin))
