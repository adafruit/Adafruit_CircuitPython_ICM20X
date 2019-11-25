import time
import board
import busio
import adafruit_icm20649

i2c = busio.I2C(board.SCL, board.SDA)

icm =  adafruit_icm20649.ICM20649(i2c)
print("inite'd without dying!")
# while True:
    # pass
