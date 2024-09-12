# Write your code here :-)
import sys
import random
import time
import board
import neopixel
import digitalio
from adafruit_pixel_framebuf import PixelFramebuffer
from rainbowio import colorwheel

#enable the boost converter
#threeV = digitalio.DigitalInOut(board.GP7)
#threeV.direction = digitalio.Direction.OUTPUT
#threeV.value = True

#the buttons do not have external pull-ups, so enable them on the rp2040
btnX = digitalio.DigitalInOut(board.GP22)
btnX.direction = digitalio.Direction.INPUT
btnX.pull = digitalio.Pull.UP

btnY = digitalio.DigitalInOut(board.GP27)
btnY.direction = digitalio.Direction.INPUT
btnY.pull = digitalio.Pull.UP

#screen dimensions are sized for the WS2812 PMod
#TODO: change this to 16x12 for BadgeSAO hardware
pixel_pin = board.GP12
pixel_width = 16
pixel_height = 12

num_pixels = pixel_width * pixel_height

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

#This is about the right brightness for indoor play, note that dynamic range is lost
#1.0 is overpoweringly bright
pixels.brightness = 0.1

#This framebuffer arangement is for the WS2812 PMod
#TODO: change this for BadgeSAO hardware
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

#a simple and very crappy single player pong-type game
#really just a demo of how to use the LEDs as a display
def pong():
    paddlePos = 0
    ballx = 0
    bally = 0
    ballxinc = 1
    ballyinc = 1
    cw = 0

    while True:
        #keep track of where the ball was last frame so that we can erase that
        #one pixel instead of blanking the entire screen
        lastballx = ballx
        lastbally = bally

        #if the ball hits the three walls or the paddle, just reverse its direction
        if ballx == 0 and bally <= paddlePos + 1 and bally >= paddlePos - 1 :
            ballxinc = 1
        elif ballx == 0 and (bally > paddlePos + 1 or bally < paddlePos - 1) :
            sys.exit() #game over if you miss the ball
        elif ballx == pixel_width-1:
            ballxinc = -1

        if bally == 0:
            ballyinc = 1
        elif bally == pixel_height-1:
            ballyinc = -1

        #the game loop is so slow that we don't worry about debouncing
        #the right way to do this would be to use the CircuitPython Keypad
        #facility to asynchronously detect transitions and then consume the
        #event queue
        if btnX.value == 0 and btnY.value == 1 and paddlePos < pixel_height-1:
            paddlePos = paddlePos + 1
        elif btnY.value == 0 and btnX.value == 1 and paddlePos > 0:
            paddlePos = paddlePos - 1

        #change the ball color for fun
        cw = 0 if cw == 256 else cw + 1

        #draw the paddle
        pixel_framebuf.vline(0, 0, pixel_height, 0x000000)
        pixel_framebuf.vline(0, paddlePos - 1, 3, 0x202020)

        #I felt that the ball moved too fast relative to the paddle,
        #so update its position every other frame to slow it down
        if cw % 2 == 0:
            ballx = ballx + ballxinc
            bally = bally + ballyinc
            pixel_framebuf.pixel(ballx,bally,colorwheel(cw)) #draw the new ball
            pixel_framebuf.pixel(lastballx,lastbally,0x000000) #erase the old ball

        pixel_framebuf.display() #send the framebuffer to the LEDs
        time.sleep(0.03)

while True:
    pong()


