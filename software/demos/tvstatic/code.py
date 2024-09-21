# Write your code here :-)
import sys
import random
import time
import board
import neopixel
import digitalio
from adafruit_pixel_framebuf import PixelFramebuffer

pixel_pin = board.GP12
pixel_width = 16
pixel_height = 12

num_pixels = pixel_width * pixel_height

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

pixels.brightness = 1.0

pixel_framebuf = PixelFramebuffer(
pixels,
pixel_width,
pixel_height,
reverse_x=True,
reverse_y=False,
alternating=False,
rotation=2
)

#blank the display
pixel_framebuf.fill(0x000000)
pixel_framebuf.display()

def static():
    while True:
        for x in range(pixel_width):
            for y in range(pixel_height):
                rval = random.randint(1,4)
                pixel_framebuf.pixel(x,y,(rval,rval,rval))

        pixel_framebuf.display() #send the framebuffer to the LEDs

while True:
    static()


