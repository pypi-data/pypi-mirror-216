# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_vcnl4010 import vcnl4010

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
vcn = vcnl4010.VCNL4010(i2c)

vcn.ambient_light_rate = vcnl4010.AMBIENT_LIGHT_RATE2

while True:
    for ambient_light_rate in vcnl4010.ambient_light_rate_values:
        print("Current Ambient light rate setting: ", vcn.ambient_light_rate)
        for _ in range(10):
            light = vcn.light
            print("Proximity: {}".format(vcn.proximity))
            print("Ambient light: {} lux".format(vcn.ambient))
            print()
            time.sleep(0.5)
        vcn.ambient_light_rate = ambient_light_rate
