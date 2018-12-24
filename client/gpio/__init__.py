"""
GPIO controller library - used to control and monitor board's GPIO pins.
This library uses slightly modified WiringPI-Python-OP library (https://github.com/lanefu/WiringPi-Python-OP) -
Orange PI adaptation of RaspberyPI's WiringPI library, which provides extensive API capabilities.
"""
from client.gpio.controller import GpioController

gpio_controller = GpioController()
