import board
import digitalio
import array
import time
import math
import bitbangio
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33

#TODO: remove GP16 and GP17. For rev1 layout these are
#permanently connected for I2C operation

#TODO: change to hardware I2C for rev1

#I2C address = 0x6A
i2ca = digitalio.DigitalInOut(board.GP16)
i2ca.direction = digitalio.Direction.OUTPUT
i2ca.value = False

#keep cs line high for i2c mode
cs = digitalio.DigitalInOut(board.GP17)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True

i2c = bitbangio.I2C(board.GP18, board.GP19, frequency = 100000)
#while not i2c.try_lock():
#    pass
#print(i2c.scan())
sensor = LSM6DS33(i2c)
acc_x, acc_y, acc_z = sensor.acceleration
gyro_x, gyro_y, gyro_z = sensor.gyro
print(acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z)

i2c.deinit()
