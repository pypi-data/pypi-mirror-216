# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_mmr902 import mmr902

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mmr = mmr902.MMR902(i2c)

while True:
    print("Pressure: {}mmHg".format(mmr.pressure))
    print("Temperature: {}C".format(mmr.temperature))
    print()
    time.sleep(0.5)
