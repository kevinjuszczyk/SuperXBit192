import sys
import time
import board
import neopixel
import digitalio
import asyncio
import keypad
from adafruit_pixel_framebuf import PixelFramebuffer
from rainbowio import colorwheel

#game state
class Pong1:
    def __init__(self, screen_width, screen_height):
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self.reset()
        
    def reset(self):
        self.paddle_pos = 1
        self.ball_x = 1
        self.ball_y = 1
        self.ball_xinc = 1
        self.ball_yinc = 1
        self.ball_color = 1
        self.pin_up_cnt = 0
        self.pin_down_cnt = 0
        self.pin_sel_cnt = 0
        self.score = 0
        self.game_over = False

async def monitor_buttons(pin_up, pin_down, pin_sel, game_state):
    with keypad.Keys(
        (pin_up, pin_down, pin_sel), value_when_pressed=False, pull=True
    ) as keys:
        while True:
            key_event = keys.events.get()
            if key_event and key_event.pressed:
                if key_event.key_number == 1 and game_state.paddle_pos < game_state.screen_height - 1:
                    game_state.pin_down_cnt += 1
                elif key_event.key_number == 0 and game_state.paddle_pos > 0:
                    game_state.pin_up_cnt += 1
                elif key_event.key_number == 2:
                    game_state.reset()   
            elif key_event and key_event.released:
                if key_event.key_number == 1:
                    game_state.pin_down_cnt = 0
                elif key_event.key_number == 0:
                    game_state.pin_up_cnt = 0
            #the fact that the following are conflated shouldn't be an issue
            #since the player should only be pressing one button at a time
            else: 
                if game_state.pin_down_cnt > 0:
                    game_state.pin_down_cnt += 1
                if game_state.pin_up_cnt > 0:
                    game_state.pin_up_cnt += 1
                
            #adjust key_pause and sleep time for best feel
            key_pause = 7
            if (game_state.pin_down_cnt == 1 or game_state.pin_down_cnt > key_pause) and game_state.paddle_pos < game_state.screen_height - 1 and game_state.pin_down_cnt%4==0:
                game_state.paddle_pos += 1
            elif (game_state.pin_up_cnt == 1 or game_state.pin_up_cnt > key_pause) and game_state.paddle_pos > 0 and game_state.pin_up_cnt%4==0:
                game_state.paddle_pos -= 1
            
            await asyncio.sleep(0.0075)

async def game_update(game_state, framebuf):
    while True:
        #keep track of where the ball was last frame so that we can erase that
        #one pixel instead of blanking the entire screen
        last_ball_x = game_state.ball_x
        last_ball_y = game_state.ball_y

        #if the ball hits the three walls or the paddle, just reverse its direction
        if game_state.ball_x == 0 and game_state.ball_y <= game_state.paddle_pos + 1 and game_state.ball_y >= game_state.paddle_pos - 1 :
            game_state.ball_xinc = 1
            game_state.score += 1
        elif game_state.ball_x == 0 and (game_state.ball_y > game_state.paddle_pos + 1 or game_state.ball_y < game_state.paddle_pos - 1):
            game_state.game_over = True #game over if you miss the ball
        elif game_state.ball_x == game_state.screen_width-1:
            game_state.ball_xinc = -1

        if game_state.ball_y == 0:
            game_state.ball_yinc = 1
        elif game_state.ball_y == game_state.screen_height-1:
            game_state.ball_yinc = -1

        #change the ball color for fun
        game_state.ball_color = 0 if game_state.ball_color == 256 else game_state.ball_color + 1

        #draw the paddle
        framebuf.vline(0, 0, game_state.screen_height, 0x000000)
        framebuf.vline(0, game_state.paddle_pos - 1, 3, 0x202020)

        #draw the ball
        game_state.ball_x = game_state.ball_x + game_state.ball_xinc
        game_state.ball_y = game_state.ball_y + game_state.ball_yinc
        framebuf.pixel(last_ball_x,last_ball_y,0x000000) #erase the old ball
        framebuf.pixel(game_state.ball_x,game_state.ball_y,colorwheel(game_state.ball_color)) #draw the new ball
        
        framebuf.display() #send the framebuffer to the LEDs
        
        while game_state.game_over:
            score = game_state.score #save this before it is reset
            await asyncio.sleep(0.06)
            framebuf.text('{:02d}'.format(score),3,2,0x000020 if game_state.game_over else 0)
            framebuf.display()
            
        #15 fps
        await asyncio.sleep(0.06)

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

async def main():
    game = Pong1(16,12)

    button_task = asyncio.create_task(monitor_buttons(pin_up = board.GP21, pin_down = board.GP26, pin_sel = board.GP28, game_state = game))

    game_task = asyncio.create_task(game_update(game, pixel_framebuf))
    
    # This will run forever, because neither task ever exits. 
    await asyncio.gather(button_task, game_task)

asyncio.run(main())