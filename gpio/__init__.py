"""
GPIO controller library - used to control and monitor board's GPIO pins.
This library uses slightly modified WiringPI-Python-OP library (https://github.com/lanefu/WiringPi-Python-OP) -
Orange PI adaptation of RaspberyPI's WiringPI library, which provides extensive API capabilities.
For now, this library it configured to work with Orange PI Lite PC (Allwinner Cortex H3 processor).
"""
from gpio.controller import GpioController

gpio_controller = GpioController()
