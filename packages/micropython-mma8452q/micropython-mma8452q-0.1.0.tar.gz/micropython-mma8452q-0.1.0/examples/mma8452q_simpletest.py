# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_mma8452q import mma8452q

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
mma = mma8452q.MMA8452Q(i2c)

while True:
    x, y, z = mma.acceleration
    print(
        "Acceleration: X={0:0.1f}m/s^2 y={1:0.1f}m/s^2 z={2:0.1f}m/s^2".format(x, y, z)
    )
    print()
    time.sleep(0.5)
