import time
import board
import busio
import adafruit_icm20649
from adafruit_debug_i2c import DebugI2C



# i2c = DebugI2C(busio.I2C(board.SCL , board.SDA))
i2c = busio.I2C(board.SCL, board.SDA)

icm =  adafruit_icm20649.ICM20649(i2c)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(icm.acceleration))
    # print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(sox.gyro))
    # print("")
    time.sleep(0.5)
