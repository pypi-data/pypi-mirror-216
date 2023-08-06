# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`tcs3430`
================================================================================

MicroPython driver for the AMS TCS3430 Color and ALS sensor


* Author(s): Jose D. Montoya


"""

from micropython import const
from micropython_tcs3430.i2c_helpers import CBits, RegisterStruct

__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_TCS3430.git"

_REG_WHOAMI = const(0x92)
_ENABLE_REGISTER = const(0x80)
_TIME = const(0x81)
_WTIME = const(0x82)
_CFG0 = const(0x8D)
_CFG1 = const(0x90)
_DATA = const(0x94)

DISABLED = const(0b00)
ENABLED = const(0b11)
operation_mode_values = (DISABLED, ENABLED)

ALS_GAIN1 = const(0b00)
ALS_GAIN4 = const(0b01)
ALS_GAIN16 = const(0b10)
ALS_GAIN64 = const(0b11)
als_gain_values = (ALS_GAIN1, ALS_GAIN4, ALS_GAIN16, ALS_GAIN64)


class TCS3430:
    """Driver for the TCS3430 Sensor connected over I2C.
    Ambient Light Sensing (ALS) and CIE 1931 Tristimulus Color Sensing (XYZ).
    These measurements can be used to calculate chromaticity,

    :param ~machine.I2C i2c: The I2C bus the TCS3430 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x39`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`TCS3430` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_tcs3430 import tcs3430

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        tcs3430 = tcs3430.TCS3430(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    _device_id = RegisterStruct(_REG_WHOAMI, "B")
    info_needed = RegisterStruct(_ENABLE_REGISTER, "B")

    _operation_mode = CBits(2, _ENABLE_REGISTER, 0)
    _integration_time = RegisterStruct(_TIME, "B")
    _als_wait_time = RegisterStruct(_WTIME, "B")
    _wait_long = CBits(1, _CFG0, 2)
    _als_gain = CBits(2, _CFG1, 0)
    _raw_data = RegisterStruct(_DATA, ">HHHH")

    _waiting_times = {0: 2.78, 1: 33.4}

    def __init__(self, i2c, address: int = 0x39) -> None:
        self._i2c = i2c
        self._address = address

        if self._device_id != 0xDC:
            raise RuntimeError("Failed to find TCS3430")
        print(bin(self.info_needed))
        self._operation_mode = ENABLED
        print(self._integration_time)

    @property
    def operation_mode(self) -> str:
        """
        Sensor operation_mode

        +------------------------------+------------------+
        | Mode                         | Value            |
        +==============================+==================+
        | :py:const:`tcs3430.DISABLED` | :py:const:`0b00` |
        +------------------------------+------------------+
        | :py:const:`tcs3430.ENABLED`  | :py:const:`0b11` |
        +------------------------------+------------------+
        """
        values = ("DISABLED", "ENABLED")
        return values[self._operation_mode]

    @operation_mode.setter
    def operation_mode(self, value: int) -> None:
        if value not in operation_mode_values:
            raise ValueError("Value must be a valid operation_mode setting")
        self._operation_mode = value

    @property
    def integration_time(self) -> float:
        """
        Integration time in 2.78ms intervals. 0x00 indicates 2.78ms,
        0x01 indicates 5.56ms.
        The maximum ALS value depends on the integration time. For
        every 2.78ms, the maximum value increases by 1024. This means
        that to be able to reach ALS full scale, the integration time has to be
        at least 64*2.78ms.
        """
        return self._integration_time * 2.78

    @integration_time.setter
    def integration_time(self, value: float) -> None:
        if value > 711 or value < 2.78:
            raise ValueError("Value must be a valid integration_time setting")
        self._integration_time = int(value / 2.78)

    @property
    def als_wait_time(self) -> float:
        """
        The wait timer is implemented with a down counter with 0x00
        as the terminal count. Loading 0x00 will generate a 2.78ms wait
        time, loading 0x01 will generate a 5.56ms wait time, and so
        forth; By asserting wlong, in register 0x8D the wait time is given
        in multiples of 33.4ms (12x)
        """
        return self._als_wait_time * self._waiting_times[self._wait_long]

    @als_wait_time.setter
    def als_wait_time(self, value: float) -> None:
        if self._wait_long:
            if value > 711 or value < 2.78:
                raise ValueError("Value must be a valid als_wait_time setting")
        else:
            if value > 23747 or value < 33.4:
                raise ValueError("Value must be a valid als_wait_time setting")
        self._als_wait_time = int(value / self._waiting_times[self._wait_long])

    @property
    def als_gain(self) -> str:
        """
        Sensor als_gain

        +--------------------------------+------------------+
        | Mode                           | Value            |
        +================================+==================+
        | :py:const:`tcs3430.ALS_GAIN1`  | :py:const:`0b00` |
        +--------------------------------+------------------+
        | :py:const:`tcs3430.ALS_GAIN4`  | :py:const:`0b01` |
        +--------------------------------+------------------+
        | :py:const:`tcs3430.ALS_GAIN16` | :py:const:`0b10` |
        +--------------------------------+------------------+
        | :py:const:`tcs3430.ALS_GAIN64` | :py:const:`0b11` |
        +--------------------------------+------------------+
        """
        values = ("ALS_GAIN1", "ALS_GAIN4", "ALS_GAIN16", "ALS_GAIN64")
        return values[self._als_gain]

    @als_gain.setter
    def als_gain(self, value: int) -> None:
        if value not in als_gain_values:
            raise ValueError("Value must be a valid als_gain setting")
        self._als_gain = value

    @property
    def measurements(self):
        """
        Return ALS values
        """
        als_z, als_y, ir1_value, als_x = self._raw_data
        return als_z, als_y, als_x, ir1_value
