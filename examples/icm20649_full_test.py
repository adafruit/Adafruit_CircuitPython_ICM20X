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
# for div in [0, 10, 255, 4096]:
#     print(div)
#     ism.accelerometer_data_rate = div
#     ism.accelerometer_data_rate
#     time.sleep(1)

# print()
# print()
# print()
# for div_g in [0, 10, 255]:
#     print(div_g)
#     ism.gyro_data_rate = div_g
#     ism.gyro_data_rate
#     time.sleep(1)

ism.gyro_data_rate = 125
ism.accelerometer_data_rate = 4095
ism.gyro_data_rate
ism.accelerometer_data_rate
st = time.monotonic()
while (time.monotonic()-st < 0.250):

    print("Accel X:%.2f Y:%.2f Z:%.2f ms^2 Gyro X:%.2f Y:%.2f Z:%.2f degrees/s"%(ism.acceleration+ism.gyro))

#     acceleration = ism.acceleration
#     # ax_max = printNewMax(acceleration[0], ax_max, "AX")
#     # ay_max = printNewMax(acceleration[1], ay_max, "AY")
#     # az_max = printNewMax(acceleration[2], az_max, "AZ")
#     gyro = ism.gyro

#     # gx_max = printNewMax(gyro[0], gx_max, "GX")
#     # gy_max = printNewMax(gyro[1], gy_max, "GY")
#     # gz_max = printNewMax(gyro[2], gz_max, "GZ")
