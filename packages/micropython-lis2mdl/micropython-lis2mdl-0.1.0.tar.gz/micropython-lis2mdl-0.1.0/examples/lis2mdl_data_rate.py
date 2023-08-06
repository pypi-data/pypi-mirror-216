# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_lis2mdl import lis2mdl

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
lis = lis2mdl.LIS2MDL(i2c)

lis.data_rate = lis2mdl.RATE_100_HZ

while True:
    for data_rate in lis2mdl.data_rate_values:
        print("Current Data rate setting: ", lis.data_rate)
        for _ in range(10):
            magx, magy, magz = lis.magnetic
            print("x:{:.2f}uT, y:{:.2f}uT, z:{:.2f}uT".format(magx, magy, magz))
            print()
            time.sleep(0.5)
        lis.data_rate = data_rate
