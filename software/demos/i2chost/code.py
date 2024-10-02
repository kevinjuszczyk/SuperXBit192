import time
import board
import busio
import digitalio

sclpu = digitalio.DigitalInOut(board.GP3)
sclpu.direction = digitalio.Direction.OUTPUT
sclpu.value = True

sdapu = digitalio.DigitalInOut(board.GP2)
sdapu.direction = digitalio.Direction.OUTPUT
sdapu.value = True

i2c = busio.I2C(board.GP5, board.GP4)

while not i2c.try_lock():
    pass
print(i2c.scan())

buffer = bytearray(1)
buffer[0] = ord('T')
i2c.writeto(0x41, buffer)
i2c.readfrom_into(0x41, buffer)
print(chr(buffer[0]))
i2c.unlock()
i2c.deinit()