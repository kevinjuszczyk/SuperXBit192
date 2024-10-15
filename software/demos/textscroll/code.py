import sys
import board
import neopixel
import digitalio
import keypad
from adafruit_pixel_framebuf import PixelFramebuffer
from rainbowio import colorwheel

def drawHackLogo(fb, x, y, color):
    fb.pixel(1+x, 0+y, color)
    fb.pixel(0+x, 1+y, color)
    fb.pixel(1+x, 1+y, color)
    fb.pixel(2+x, 2+y, color)
    fb.pixel(3+x, 3+y, color)

    fb.pixel(11+x, 0+y, color)
    fb.pixel(11+x, 1+y, color)
    fb.pixel(12+x, 1+y, color)
    fb.pixel(10+x, 2+y, color)
    fb.pixel(9+x, 3+y, color)

    fb.pixel(0+x, 10+y, color)
    fb.pixel(1+x, 10+y, color)
    fb.pixel(1+x, 11+y, color)
    fb.pixel(2+x, 9+y, color)
    fb.pixel(3+x, 8+y, color)

    fb.pixel(11+x, 11+y, color)
    fb.pixel(11+x, 10+y, color)
    fb.pixel(12+x, 10+y, color)
    fb.pixel(10+x, 9+y, color)
    fb.pixel(9+x, 8+y, color)
    
    fb.hline(5+x, 3+y, 3, color)
    fb.hline(4+x, 4+y, 5, color)
    
    fb.vline(6+x, 5+y, 2, color)
    fb.vline(3+x, 5+y, 2, color)
    fb.vline(9+x, 5+y, 2, color)
    fb.vline(5+x, 6+y, 4, color)
    fb.vline(7+x, 6+y, 4, color)
    
    fb.pixel(6+x, 8+y, color)
    fb.pixel(4+x, 7+y, color)
    fb.pixel(8+x, 7+y, color)
    

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

cw = 0
charw = 6
s = "Supercon 8"

while True:
    for x in range(pixel_width, -len(s) * charw, -1):
        pixel_framebuf.text(s,x+1,2,0)
        pixel_framebuf.text(s,x,2,colorwheel(cw))
        pixel_framebuf.display()
        cw = 0 if cw == 256 else cw + 1

    for x in range(pixel_width, 0, -1):
        drawHackLogo(pixel_framebuf, x+1, 0, 0)
        drawHackLogo(pixel_framebuf, x, 0, 0xf0f0f0)
        pixel_framebuf.display()

    for x in range(0, 3, 1):
        drawHackLogo(pixel_framebuf, x-1, 0, 0)
        drawHackLogo(pixel_framebuf, x, 0, 0xf0f0f0)
        pixel_framebuf.display()

    for x in range(3, -14, -1):
        drawHackLogo(pixel_framebuf, x+1, 0, 0)
        drawHackLogo(pixel_framebuf, x, 0, 0xf0f0f0)
        pixel_framebuf.display()
