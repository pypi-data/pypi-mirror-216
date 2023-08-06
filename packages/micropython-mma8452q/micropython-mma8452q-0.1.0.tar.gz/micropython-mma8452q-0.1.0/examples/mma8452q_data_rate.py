# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_mma8452q import mma8452q

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mma = mma8452q.MMA8452Q(i2c)

mma.data_rate = mma8452q.DATARATE_800HZ

while True:
    for data_rate in mma8452q.data_rate_values:
        print("Current Data rate setting: ", mma.data_rate)
        for _ in range(10):
            accx, accy, accz = mma.acceleration
            print("x:{:.2f}m/s2, y:{:.2f}m/s2, z:{:.2f}m/s2".format(accx, accy, accz))
            print()
            time.sleep(0.5)
        mma.data_rate = data_rate
