import sys
import time
import board
import neopixel
import digitalio
import asyncio
import keypad
import random
from adafruit_pixel_framebuf import PixelFramebuffer


class Pipe:
    def __init__(self, x, h, w):
        self.x = x
        self.h = h
        self.w = w
        self.old_x = x
        
#game state
class FloppyBit:
    def __init__(self, screen_width, screen_height):
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self.reset()
        
    def reset(self):
        self.global_acc = 0.08
        self.bit_acc = 0.4
        self.bit_vel = 0
        self.bit_ypos = 5.0
        self.bit_ypix = 5
        self.bit_xpix = 2
        self.old_bit_ypix = -1
        self.pipes = [Pipe(16, 5, 4), Pipe(24, 7, 4)]
        self.score = 0
        self.game_over = False
        self.game_started = False

async def monitor_buttons(pin_up, pin_sel, game_state):
    with keypad.Keys(
        (pin_up, pin_sel), value_when_pressed=False, pull=True
    ) as keys:
        while True:
            key_event = keys.events.get()
            if key_event and key_event.pressed:
                if key_event.key_number == 0 and game_state.game_over == False:
                    game_state.bit_vel = 0 if game_state.bit_vel - game_state.bit_acc > 0 else game_state.bit_vel - game_state.bit_acc
                    game_state.game_started = True
            
                elif key_event.key_number == 1:
                    game_state.reset()   
            
            await asyncio.sleep(0.0075)

async def game_update(game_state, framebuf):
    pipe_move_inc = 0
    while True:
        if game_state.game_started == True:
            game_state.bit_ypos = 0 if game_state.bit_ypos + game_state.bit_vel < 0 else game_state.bit_ypos + game_state.bit_vel
            game_state.old_bit_ypix = game_state.bit_ypix
            game_state.bit_ypix = int(game_state.bit_ypos)

            game_state.bit_vel += game_state.global_acc

            if pipe_move_inc == 3:
                for p in game_state.pipes:
                    p.old_x = p.x
                    p.x -= 1
                    if p.x < 0:
                        p.x = game_state.screen_width
                        game_state.score += 1
                        p.h = random.randint(2, 7)
                        
                    #draw the pipes
                    framebuf.vline(p.old_x, 0,game_state.screen_height, 0x000000)
                    framebuf.vline(p.x, 0, p.h, 0x00FF00)
                    framebuf.vline(p.x, p.h + p.w, game_state.screen_height, 0x00FF00)

                pipe_move_inc = 0
            
            pipe_move_inc += 1

        #blank display while game is not started
        if game_state.game_started == False:
            pixel_framebuf.fill(0x000000)

        #draw the bit
        if (framebuf.pixel(game_state.bit_xpix, game_state.bit_ypix) == 0x00FF00) or game_state.bit_ypix >= game_state.screen_height:
            game_state.game_over = True
        framebuf.pixel(game_state.bit_xpix, game_state.old_bit_ypix, 0x000000)
        framebuf.pixel(game_state.bit_xpix, game_state.bit_ypix, 0xFFFF00)
        
        framebuf.display() #send the framebuffer to the LEDs
        
        while game_state.game_over:
            score = game_state.score #save this before it is reset
            await asyncio.sleep(0.03)
            framebuf.text('{:02d}'.format(score),3,2,0x0000FF if game_state.game_over else 0)
            framebuf.display()
            
        #30 fps
        await asyncio.sleep(0.03)

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

async def main():
    game = FloppyBit(16,12)

    button_task = asyncio.create_task(monitor_buttons(pin_up = board.GP21, pin_sel = board.GP28, game_state = game))

    game_task = asyncio.create_task(game_update(game, pixel_framebuf))
    
    # This will run forever, because neither task ever exits. 
    await asyncio.gather(button_task, game_task)

asyncio.run(main())