# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_lis2mdl import lis2mdl

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
lis = lis2mdl.LIS2MDL(i2c)

lis.interrupt_threshold = 80
lis.interrupt_mode = lis2mdl.INT_ENABLED

while True:
    magx, magy, magz = lis.magnetic
    print("x:{:.2f}uT, y:{:.2f}uT, z:{:.2f}uT".format(magx, magy, magz))
    print()
    if lis.interrupt_triggered:
        alert_status = lis.alert_status
        if alert_status.x_high:
            print("X axes above high set limit!")
        if alert_status.x_low:
            print("X axes below low set limit!")
    time.sleep(0.5)
