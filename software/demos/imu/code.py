import board
import digitalio
import array
import time
import math
import busio
from adafruit_lsm6ds.LSM6DS3TRC import LSM6DS3TRC

i2c = busio.I2C(board.GP19, board.GP18, frequency = 100000)
#while not i2c.try_lock():
#    pass
#print(i2c.scan())
sensor = LSM6DS3TRC(i2c)

while True:
    acc_x, acc_y, acc_z = sensor.acceleration
    gyro_x, gyro_y, gyro_z = sensor.gyro
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z))
    time.sleep(0.1)

i2c.deinit()