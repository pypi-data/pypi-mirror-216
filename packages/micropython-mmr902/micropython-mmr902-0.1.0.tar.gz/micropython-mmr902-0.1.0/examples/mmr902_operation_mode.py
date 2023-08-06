# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_mmr902 import mmr902

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mmr = mmr902.MMR902(i2c)

mmr.operation_mode = mmr902.MODE1

while True:
    for operation_mode in mmr902.operation_mode_values:
        print("Current Operation mode setting: ", mmr.operation_mode)
        for _ in range(10):
            press = mmr.pressure
            print("Temperature: {:.2f}mmHg".format(press))
            print()
            time.sleep(0.5)
        mmr.operation_mode = operation_mode
