import time
import board
import busio
import adafruit_icm20649

i2c = busio.I2C(board.SCL, board.SDA)
icm =  adafruit_icm20649.ICM20649(i2c)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(icm.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(icm.gyro))
    print("")
    time.sleep(0.5)
