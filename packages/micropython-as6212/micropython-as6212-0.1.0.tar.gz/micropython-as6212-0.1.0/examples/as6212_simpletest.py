# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_as6212 import as6212

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
as6 = as6212.AS6212(i2c)

while True:
    print(f"Temperature: {as6.temperature:.2f}C")
    time.sleep(0.5)
