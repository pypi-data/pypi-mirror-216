# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`mmr902`
================================================================================

MicroPython Driver fro the Mitsumi MMR902 Micro Pressure Sensor


* Author(s): Jose D. Montoya


"""
import time
from micropython import const


__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_MMR902.git"


MODE1 = const(0xA0)
MODE2 = const(0xA2)
MODE3 = const(0xA4)
MODE4 = const(0xA6)
operation_mode_values = (MODE1, MODE2, MODE3, MODE4)
_temp_waiting_values = {MODE1: 0.034, MODE2: 0.021, MODE3: 0.014, MODE4: 0.439}
_press_waiting_values = {MODE1: 0.016, MODE2: 0.08, MODE3: 0.004, MODE4: 0.256}


class MMR902:
    """Driver for the MMR902 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the MMR902 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x65`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`MMR902` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_mmr902 import mmr902

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        mmr902 = mmr902.MMR902(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    def __init__(self, i2c, address: int = 0x65) -> None:
        self._i2c = i2c
        self._address = address
        self._temp_waiting = None
        self._press_waiting = None
        self.operation_mode = MODE1

    @property
    def pressure(self) -> float:
        """
        Pressure in mmHg
        """
        data = bytearray(3)
        self._i2c.writeto(self._address, bytes([0xC0]))
        time.sleep(self._press_waiting)
        self._i2c.readfrom_into(self._address, data)
        result = data[0] << 16 | data[1] << 8 | data[2]

        return self._twos_comp(result, 24) / 1000

    @property
    def temperature(self) -> float:
        """
        Temperature in Celsius
        """
        data = bytearray(3)
        self._i2c.writeto(self._address, bytes([0xC2]))
        time.sleep(self._temp_waiting)
        self._i2c.readfrom_into(self._address, data)
        result = data[0] << 16 | data[1] << 8 | data[2]

        return self._twos_comp(result, 24) / 2**16.0

    @staticmethod
    def _twos_comp(val: int, bits: int) -> int:
        if val & (1 << (bits - 1)) != 0:
            return val - (1 << bits)
        return val

    @property
    def operation_mode(self) -> str:
        """
        Sensor operation_mode

        +--------------------------+------------------+
        | Mode                     | Value            |
        +==========================+==================+
        | :py:const:`mmr902.MODE1` | :py:const:`0XA0` |
        +--------------------------+------------------+
        | :py:const:`mmr902.MODE2` | :py:const:`0XA2` |
        +--------------------------+------------------+
        | :py:const:`mmr902.MODE3` | :py:const:`0XA4` |
        +--------------------------+------------------+
        | :py:const:`mmr902.MODE4` | :py:const:`0XA6` |
        +--------------------------+------------------+
        """
        values = {MODE1: "MODE1", MODE2: "MODE2", MODE3: "MODE3", MODE4: "MODE4"}
        return values[self._command]

    @operation_mode.setter
    def operation_mode(self, value: int) -> None:
        if value not in operation_mode_values:
            raise ValueError("Value must be a valid operation_mode setting")
        self._command = value
        self._temp_waiting = _temp_waiting_values[value]
        self._press_waiting = _press_waiting_values[value]
        self._i2c.writeto(self._address, bytes([self._command]))
