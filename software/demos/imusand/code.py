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

acc_den = 100.0
vel_term = 0.99 #do not allow more than one pixel displacement per frame
num_parts = 36

class Particle:
    def __init__(self, color, pix_x, pix_y, pos_x, pos_y, vel_x, vel_y, min_x, min_y, max_x, max_y):
        self.color = color
        self.pix_x = pix_x
        self.pix_y = pix_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def think(self, fbuf, acc_x, acc_y):
        old_pix_x = self.pix_x
        old_pix_y = self.pix_y
        
        self.pos_x += min(self.vel_x, vel_term) if self.vel_x > 0 else max(self.vel_x, -vel_term)
        self.pos_y += min(self.vel_y, vel_term) if self.vel_y > 0 else max(self.vel_y, -vel_term)
        self.pix_x = int(self.pos_x)
        self.pix_y = int(self.pos_y)
        self.vel_x += -acc_x/acc_den
        self.vel_y += acc_y/acc_den

        #check for screen bounds
        if self.pix_x < self.min_x:
            self.pos_x = self.min_x
            self.pix_x = self.min_x
            self.vel_x = 0.0
        elif self.pix_x > self.max_x:
            self.pos_x = self.max_x
            self.pix_x = self.max_x
            self.vel_x = 0.0

        if self.pix_y < self.min_y:
            self.pos_y = self.min_y
            self.pix_y = self.min_y
            self.vel_y = 0.0
        elif self.pix_y > self.max_y:
            self.pos_y = self.max_y
            self.pix_y = self.max_y
            self.vel_y = 0.0

        #check for collisions
        if fbuf.pixel(self.pix_x, self.pix_y) != 0:
            self.vel_x = 0 if fbuf.pixel(self.pix_x, old_pix_y) != 0 else self.vel_x
            self.vel_y = 0 if fbuf.pixel(old_pix_x, self.pix_y) != 0 else self.vel_y
            self.pos_x = old_pix_x
            self.pos_y = old_pix_y
            self.pix_x = old_pix_x
            self.pix_y = old_pix_y


#display setup
pixel_pin = board.GP12
pixel_width = 16
pixel_height = 12
num_pixels = pixel_width * pixel_height

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

#This is about the right brightness for indoor play, note that dynamic range is lost
#1.0 is overpoweringly bright
pixels.brightness = 0.025

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

colors = []
for c in range(num_parts):
    colors.append(colorwheel(c*256/num_parts))

pars = []
for i in range(len(colors)):
    pars.append(Particle(colors[i], i, i, float(i), float(i), 0.0, 0.0, 0, 0, 15, 11))

while True:
    acc_x, acc_y, acc_z = sensor.acceleration
    gyro_x, gyro_y, gyro_z = sensor.gyro
    #print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z))

    for p in pars:     
        pixel_framebuf.pixel(p.pix_x, p.pix_y, 0)
        p.think(pixel_framebuf, acc_x, acc_y)  
        pixel_framebuf.pixel(p.pix_x, p.pix_y, p.color)

    pixel_framebuf.display()

i2c.deinit()
