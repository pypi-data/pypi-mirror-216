# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`vcnl4010`
================================================================================

MicroPython Driver for the Vishay VCNL4010 Proximity and Ambient Light Sensor


* Author(s): Jose D. Montoya


"""

import time
from micropython import const
from micropython_vcnl4010.i2c_helpers import CBits, RegisterStruct


__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_VCNL4010.git"

_REG_WHOAMI = const(0x81)
_COMMAND_REGISTER = const(0x80)
_PROXIMITY_RATE_REGISTER = const(0x82)
_IR_LED_CURRENT_REGISTER = const(0x83)
_AMBIENT_LIGHT_PARAMETER_REGISTER = const(0x84)
_AMBIENT_LIGHT_DATA = const(0x85)
_PROXIMITY_DATA = const(0x87)

SAMPLERATE_1_95 = const(0b000)
SAMPLERATE_3_90625 = const(0b001)
SAMPLERATE_7_8125 = const(0b010)
SAMPLERATE_16_625 = const(0b011)
SAMPLERATE_31_25 = const(0b100)
SAMPLERATE_62_5 = const(0b101)
SAMPLERATE_125 = const(0b110)
SAMPLERATE_250 = const(0b111)
proximity_rate_values = (
    SAMPLERATE_1_95,
    SAMPLERATE_3_90625,
    SAMPLERATE_7_8125,
    SAMPLERATE_16_625,
    SAMPLERATE_31_25,
    SAMPLERATE_62_5,
    SAMPLERATE_125,
    SAMPLERATE_250,
)

AMBIENT_LIGHT_RATE1 = const(0b000)
AMBIENT_LIGHT_RATE2 = const(0b001)
AMBIENT_LIGHT_RATE3 = const(0b010)
AMBIENT_LIGHT_RATE4 = const(0b011)
AMBIENT_LIGHT_RATE5 = const(0b100)
AMBIENT_LIGHT_RATE6 = const(0b101)
AMBIENT_LIGHT_RATE8 = const(0b110)
AMBIENT_LIGHT_RATE10 = const(0b111)
ambient_light_rate_values = (
    AMBIENT_LIGHT_RATE1,
    AMBIENT_LIGHT_RATE2,
    AMBIENT_LIGHT_RATE3,
    AMBIENT_LIGHT_RATE4,
    AMBIENT_LIGHT_RATE5,
    AMBIENT_LIGHT_RATE6,
    AMBIENT_LIGHT_RATE8,
    AMBIENT_LIGHT_RATE10,
)

AL_AVERAGE1 = const(0b000)
AL_AVERAGE2 = const(0b001)
AL_AVERAGE4 = const(0b010)
AL_AVERAGE8 = const(0b011)
AL_AVERAGE16 = const(0b100)
AL_AVERAGE32 = const(0b101)
AL_AVERAGE64 = const(0b110)
AL_AVERAGE128 = const(0b111)
ambient_light_average_values = (
    AL_AVERAGE1,
    AL_AVERAGE2,
    AL_AVERAGE4,
    AL_AVERAGE8,
    AL_AVERAGE16,
    AL_AVERAGE32,
    AL_AVERAGE64,
    AL_AVERAGE128,
)


class VCNL4010:
    """Driver for the VCNL4010 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the VCNL4010 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x13`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`VCNL4010` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_vcnl4010 import vcnl4010

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        vcnl4010 = vcnl4010.VCNL4010(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    _device_id = RegisterStruct(_REG_WHOAMI, "B")
    _ambient_light = RegisterStruct(_AMBIENT_LIGHT_DATA, "H")
    _proximity = RegisterStruct(_PROXIMITY_DATA, "H")

    _proximity_rate = CBits(3, _PROXIMITY_RATE_REGISTER, 0)

    _ambient_light_measure_ready = CBits(1, _COMMAND_REGISTER, 6)
    _proximity_measure_ready = CBits(1, _COMMAND_REGISTER, 5)
    _get_ambient_light = CBits(1, _COMMAND_REGISTER, 4)
    _get_proximity = CBits(1, _COMMAND_REGISTER, 3)

    _ambient_light_rate = CBits(3, _AMBIENT_LIGHT_PARAMETER_REGISTER, 4)
    _ambient_light_average = CBits(3, _AMBIENT_LIGHT_PARAMETER_REGISTER, 0)

    _irl_led_current = CBits(6, _IR_LED_CURRENT_REGISTER, 0)

    def __init__(self, i2c, address: int = 0x13) -> None:
        self._i2c = i2c
        self._address = address

        if self._device_id != 0x21:
            raise RuntimeError("Failed to find VCNL4010")

    @property
    def proximity_rate(self) -> str:
        """
        Sensor proximity_rate

        +-----------------------------------------+-------------------+
        | Mode                                    | Value             |
        +=========================================+===================+
        | :py:const:`vcnl4010.SAMPLERATE_1_95`    | :py:const:`0b000` |
        +-----------------------------------------+-------------------+
        | :py:const:`vcnl4010.SAMPLERATE_3_90625` | :py:const:`0b001` |
        +-----------------------------------------+-------------------+
        | :py:const:`vcnl4010.SAMPLERATE_7_8125`  | :py:const:`0b010` |
        +-----------------------------------------+-------------------+
        | :py:const:`vcnl4010.SAMPLERATE_16_625`  | :py:const:`0b011` |
        +-----------------------------------------+-------------------+
        | :py:const:`vcnl4010.SAMPLERATE_31_25`   | :py:const:`0b100` |
        +-----------------------------------------+-------------------+
        | :py:const:`vcnl4010.SAMPLERATE_62_5`    | :py:const:`0b101` |
        +-----------------------------------------+-------------------+
        | :py:const:`vcnl4010.SAMPLERATE_125`     | :py:const:`0b110` |
        +-----------------------------------------+-------------------+
        | :py:const:`vcnl4010.SAMPLERATE_250`     | :py:const:`0b111` |
        +-----------------------------------------+-------------------+
        """
        values = (
            "SAMPLERATE_1_95",
            "SAMPLERATE_3_90625",
            "SAMPLERATE_7_8125",
            "SAMPLERATE_16_625",
            "SAMPLERATE_31_25",
            "SAMPLERATE_62_5",
            "SAMPLERATE_125",
            "SAMPLERATE_250",
        )
        return values[self._proximity_rate]

    @proximity_rate.setter
    def proximity_rate(self, value: int) -> None:
        if value not in proximity_rate_values:
            raise ValueError("Value must be a valid proximity_rate setting")
        self._proximity_rate = value

    @property
    def irl_led_current(self) -> int:
        """
        IR LED current = Value (dec.) x 10 mA.
        Valid Range = 0 to 20d. e.g. 0 = 0 mA , 1 = 10 mA, ….,
        20 = 200 mA (2 = 20 mA = DEFAULT)
        LED Current is limited to 200 mA for values higher as 20d.
        """
        return self._irl_led_current

    @irl_led_current.setter
    def irl_led_current(self, value: int) -> None:
        if value not in range(1, 21, 1):
            raise ValueError("Value must be a valid irl_led_current setting")
        self._irl_led_current = value

    @property
    def ambient_light_rate(self) -> str:
        """
        Sensor ambient_light_rate

        +-------------------------------------------+-------------------+
        | Mode                                      | Value             |
        +===========================================+===================+
        | :py:const:`vcnl4010.AMBIENT_LIGHT_RATE1`  | :py:const:`0b000` |
        +-------------------------------------------+-------------------+
        | :py:const:`vcnl4010.AMBIENT_LIGHT_RATE2`  | :py:const:`0b001` |
        +-------------------------------------------+-------------------+
        | :py:const:`vcnl4010.AMBIENT_LIGHT_RATE3`  | :py:const:`0b010` |
        +-------------------------------------------+-------------------+
        | :py:const:`vcnl4010.AMBIENT_LIGHT_RATE4`  | :py:const:`0b011` |
        +-------------------------------------------+-------------------+
        | :py:const:`vcnl4010.AMBIENT_LIGHT_RATE5`  | :py:const:`0b100` |
        +-------------------------------------------+-------------------+
        | :py:const:`vcnl4010.AMBIENT_LIGHT_RATE6`  | :py:const:`0b101` |
        +-------------------------------------------+-------------------+
        | :py:const:`vcnl4010.AMBIENT_LIGHT_RATE8`  | :py:const:`0b110` |
        +-------------------------------------------+-------------------+
        | :py:const:`vcnl4010.AMBIENT_LIGHT_RATE10` | :py:const:`0b111` |
        +-------------------------------------------+-------------------+
        """
        values = (
            "AMBIENT_LIGHT_RATE1",
            "AMBIENT_LIGHT_RATE2",
            "AMBIENT_LIGHT_RATE3",
            "AMBIENT_LIGHT_RATE4",
            "AMBIENT_LIGHT_RATE5",
            "AMBIENT_LIGHT_RATE6",
            "AMBIENT_LIGHT_RATE8",
            "AMBIENT_LIGHT_RATE10",
        )
        return values[self._ambient_light_rate]

    @ambient_light_rate.setter
    def ambient_light_rate(self, value: int) -> None:
        if value not in ambient_light_rate_values:
            raise ValueError("Value must be a valid ambient_light_rate setting")
        self._ambient_light_rate = value

    @property
    def ambient_light_average(self) -> str:
        """
        Sensor ambient_light_average

        +------------------------------------+-------------------+
        | Mode                               | Value             |
        +====================================+===================+
        | :py:const:`vcnl4010.AL_AVERAGE1`   | :py:const:`0b000` |
        +------------------------------------+-------------------+
        | :py:const:`vcnl4010.AL_AVERAGE2`   | :py:const:`0b001` |
        +------------------------------------+-------------------+
        | :py:const:`vcnl4010.AL_AVERAGE4`   | :py:const:`0b010` |
        +------------------------------------+-------------------+
        | :py:const:`vcnl4010.AL_AVERAGE8`   | :py:const:`0b011` |
        +------------------------------------+-------------------+
        | :py:const:`vcnl4010.AL_AVERAGE16`  | :py:const:`0b100` |
        +------------------------------------+-------------------+
        | :py:const:`vcnl4010.AL_AVERAGE32`  | :py:const:`0b101` |
        +------------------------------------+-------------------+
        | :py:const:`vcnl4010.AL_AVERAGE64`  | :py:const:`0b110` |
        +------------------------------------+-------------------+
        | :py:const:`vcnl4010.AL_AVERAGE128` | :py:const:`0b111` |
        +------------------------------------+-------------------+
        """
        values = (
            "AL_AVERAGE1",
            "AL_AVERAGE2",
            "AL_AVERAGE4",
            "AL_AVERAGE8",
            "AL_AVERAGE16",
            "AL_AVERAGE32",
            "AL_AVERAGE64",
            "AL_AVERAGE128",
        )
        return values[self._ambient_light_average]

    @ambient_light_average.setter
    def ambient_light_average(self, value: int) -> None:
        if value not in ambient_light_average_values:
            raise ValueError("Value must be a valid ambient_light_average setting")
        self._ambient_light_average = value

    @property
    def proximity(self) -> int:
        """
        Proximity of an object in front of the sensor
        """

        self._get_proximity = True

        while True:
            if self._proximity_measure_ready:
                return self._proximity
            time.sleep(0.001)

    @property
    def ambient(self) -> int:
        """
        Ambient light in lux
        """
        self._get_ambient_light = True

        while True:
            if self._ambient_light_measure_ready:
                return self._ambient_light * 0.25
            time.sleep(0.001)
