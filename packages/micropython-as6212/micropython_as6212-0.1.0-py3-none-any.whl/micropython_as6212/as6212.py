# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`as6212`
================================================================================

MicroPython Library for the ASM AS6212 Temperature Sensor


* Author(s): Jose D. Montoya


"""
import time
from micropython import const
from micropython_as6212.i2c_helpers import CBits, RegisterStruct


__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_AS6212.git"

_DATA = const(0x00)
_CONF = const(0x1)

RATE_0_25 = const(0b00)
RATE_1 = const(0b01)
RATE_4 = const(0b10)
RATE_8 = const(0b11)
conversion_rate_values = (RATE_0_25, RATE_1, RATE_4, RATE_8)

CONTINUOUS = const(0b0)
SLEEP = const(0b1)
operation_mode_values = (CONTINUOUS, SLEEP)


class AS6212:
    """Driver for the AS6212 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the AS6212 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x48`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`AS6212` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_as6212 import as6212

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        as6212 = as6212.AS6212(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    _conversion_rate = CBits(2, _CONF, 6, 2, False)
    _operation_mode = CBits(1, _CONF, 8, 2, False)

    _temperature_data = RegisterStruct(_DATA, ">h")

    def __init__(self, i2c, address: int = 0x48) -> None:
        self._i2c = i2c
        self._address = address

    @property
    def conversion_rate(self) -> str:
        """
        Sensor conversion_rate
        The conversion rate bits define the number of executed temperature
        conversions per time unit.
        Additional readouts of the temperature register between conversions
        are possible but not recommended because the value is changed only
        after a conversion is finished.

        +------------------------------+------------------+
        | Mode                         | Value            |
        +==============================+==================+
        | :py:const:`as6212.RATE_0_25` | :py:const:`0b00` |
        +------------------------------+------------------+
        | :py:const:`as6212.RATE_1`    | :py:const:`0b01` |
        +------------------------------+------------------+
        | :py:const:`as6212.RATE_4`    | :py:const:`0b10` |
        +------------------------------+------------------+
        | :py:const:`as6212.RATE_8`    | :py:const:`0b11` |
        +------------------------------+------------------+
        """
        values = ("RATE_0_25", "RATE_1", "RATE_4", "RATE_8")
        return values[self._conversion_rate]

    @conversion_rate.setter
    def conversion_rate(self, value: int) -> None:
        if value not in conversion_rate_values:
            raise ValueError("Value must be a valid conversion_rate setting")
        self._conversion_rate = value

    @property
    def operation_mode(self) -> str:
        """
        Sensor operation_mode
        When the sleep mode is activated, this will shut the
        device down immediately and reduces the power consumption
        to a minimum value.

        +-------------------------------+-----------------+
        | Mode                          | Value           |
        +===============================+=================+
        | :py:const:`as6212.CONTINUOUS` | :py:const:`0b0` |
        +-------------------------------+-----------------+
        | :py:const:`as6212.SLEEP`      | :py:const:`0b1` |
        +-------------------------------+-----------------+
        """
        values = ("CONTINUOUS", "SLEEP")
        return values[self._operation_mode]

    @operation_mode.setter
    def operation_mode(self, value: int) -> None:
        if value not in operation_mode_values:
            raise ValueError("Value must be a valid operation_mode setting")
        self._operation_mode = value
        if value == SLEEP:
            _ = self.temperature
            time.sleep(0.12)

    @property
    def temperature(self) -> float:
        return self._temperature_data / 128.0
