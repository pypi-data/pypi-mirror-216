# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_as6212 import as6212

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
as6 = as6212.AS6212(i2c)

as6.conversion_rate = as6212.RATE_8

while True:
    for conversion_rate in as6212.conversion_rate_values:
        print("Current Conversion rate setting: ", as6.conversion_rate)
        for _ in range(10):
            temp = as6.temperature
            print("Temperature: {:.2f}C".format(temp))
            print()
            time.sleep(0.5)
        as6.conversion_rate = conversion_rate
