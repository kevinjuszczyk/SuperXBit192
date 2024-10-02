import time
import board
import busio
import digitalio

uart = busio.UART(board.GP0, board.GP1, baudrate=9600, timeout=0)

uart.write(bytes("Hello from SuperXBit192", 'utf8'))

while True:
    byte_read = uart.read(1) 
    if byte_read:
        print(byte_read.decode())
    else:
        continue