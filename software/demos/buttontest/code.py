import board
import digitalio
import time

bootsel = digitalio.DigitalInOut(board.VOLTAGE_MONITOR)
bootsel.direction = digitalio.Direction.INPUT
bootsel.pull = digitalio.Pull.UP

up = digitalio.DigitalInOut(board.GP22)
up.direction = digitalio.Direction.INPUT
up.pull = digitalio.Pull.UP

down = digitalio.DigitalInOut(board.GP27)
down.direction = digitalio.Direction.INPUT
down.pull = digitalio.Pull.UP

left = digitalio.DigitalInOut(board.GP26)
left.direction = digitalio.Direction.INPUT
left.pull = digitalio.Pull.UP

right = digitalio.DigitalInOut(board.GP28)
right.direction = digitalio.Direction.INPUT
right.pull = digitalio.Pull.UP

a = digitalio.DigitalInOut(board.GP10)
a.direction = digitalio.Direction.INPUT
a.pull = digitalio.Pull.UP

b = digitalio.DigitalInOut(board.GP9)
b.direction = digitalio.Direction.INPUT
b.pull = digitalio.Pull.UP


bl = digitalio.DigitalInOut(board.GP6)
bl.direction = digitalio.Direction.OUTPUT
bl.value = True

while True:
    if  up.value == False or \
            down.value == False or \
            right.value == False or \
            left.value == False or \
            bootsel.value == False or \
            b.value == False or \
            a.value == False:
        bl.value = False
        print("bootsel:{}, up:{}, down:{}, left:{}, right:{}, b:{}, a:{}". \
            format(bootsel.value, up.value, down.value, \
            left.value, right.value, b.value, a.value))
    else:
        bl.value = True
        
    time.sleep(0.2)