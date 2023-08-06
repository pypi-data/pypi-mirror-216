# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_tcs3430 import tcs3430

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
tcs = tcs3430.TCS3430(i2c)

tcs.als_gain = tcs3430.ALS_GAIN16

while True:
    for als_gain in tcs3430.als_gain_values:
        print("Current Als gain setting: ", tcs.als_gain)
        for _ in range(10):
            lux = tcs.lux
            z, y, ir1, x = tcs.measurements
            print(f"x: {x}, y: {y}, z: {z}, ir1: {ir1}")
            time.sleep(0.5)
        tcs.als_gain = als_gain
