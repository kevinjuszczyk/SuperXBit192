import board
import digitalio
import array
import time
import math
import busio
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
from rainbowio import colorwheel
from adafruit_lsm6ds.LSM6DS3TRC import LSM6DS3TRC

#display setup
pixel_pin = board.GP12
pixel_width = 16
pixel_height = 12
num_pixels = pixel_width * pixel_height

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

#This is about the right brightness for indoor play, note that dynamic range is lost
#1.0 is overpoweringly bright
pixels.brightness = 0.1

pixel_framebuf = PixelFramebuffer(
pixels,
pixel_width,
pixel_height,
reverse_x=False,
reverse_y=False,
alternating=False,
rotation=2
)

#blank the display
pixel_framebuf.fill(0x000000)
pixel_framebuf.display()

i2c = busio.I2C(board.GP19, board.GP18, frequency = 100000)
#while not i2c.try_lock():
#    pass
#print(i2c.scan())
sensor = LSM6DS3TRC(i2c)

oldx = 0
oldy = 0
while True:
    acc_x, acc_y, acc_z = sensor.acceleration
    gyro_x, gyro_y, gyro_z = sensor.gyro
    #print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z))
    pixel_framebuf.line(8, 6, oldx, oldy, 0) #blank old line
    x = -acc_x//2 + 8
    y = acc_y//2 + 6
    pixel_framebuf.line(8, 6, x, y, 0xFFFFFF)
    #print("{:<15} {:<15} ".format(x, y))
    oldx = x
    oldy = y
    pixel_framebuf.display()

i2c.deinit()