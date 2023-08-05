# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_vcnl4010 import vcnl4010

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
vcn = vcnl4010.VCNL4010(i2c)

vcn.proximity_rate = vcnl4010.SAMPLERATE_31_25

while True:
    for proximity_rate in vcnl4010.proximity_rate_values:
        print("Current Proximity rate setting: ", vcn.proximity_rate)
        for _ in range(10):
            print("Proximity: {}".format(vcn.proximity))
            print("Ambient light: {} lux".format(vcn.ambient))
            print()
            time.sleep(0.5)
        vcn.proximity_rate = proximity_rate
