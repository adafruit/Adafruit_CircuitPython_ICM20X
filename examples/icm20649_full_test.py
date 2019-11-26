def printNewMax(value, max, axis):
    if value > max:
        max = value
        print(axis, "Max:", max)
    return max

import time
import board
import busio
from adafruit_icm20649 import ICM20649, AccelRange, GyroRange
from adafruit_debug_i2c import DebugI2C

i2c = busio.I2C(board.SCL, board.SDA)
# i2c = DebugI2C(busio.I2C(board.SCL , board.SDA))

ism = ICM20649(i2c)

ism.accelerometer_range = AccelRange.RANGE_30G
print("Accelerometer range set to: %d G"%AccelRange.string[ism.accelerometer_range])

ism.gyro_range = GyroRange.RANGE_500_DPS
print("Gyro range set to: %d DPS"%GyroRange.string[ism.gyro_range])

ax_max = 0
ay_max = 0
az_max = 0
gx_max = 0
gy_max = 0
gz_max = 0

# while True:
for i in range(4):

    acceleration = ism.acceleration
    # ax_max = printNewMax(acceleration[0], ax_max, "AX")
    # ay_max = printNewMax(acceleration[1], ay_max, "AY")
    # az_max = printNewMax(acceleration[2], az_max, "AZ")
    gyro = ism.gyro

    # gx_max = printNewMax(gyro[0], gx_max, "GX")
    # gy_max = printNewMax(gyro[1], gy_max, "GY")
    # gz_max = printNewMax(gyro[2], gz_max, "GZ")



    print("Accel X:%.2f Y:%.2f Z:%.2f ms^2 Gyro X:%.2f Y:%.2f Z:%.2f degrees/s"%
        (ism.acceleration+ism.gyro))