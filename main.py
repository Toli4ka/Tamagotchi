# Main file can be uplaoded to the board to run on boot.

from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)
print('Blinking LED Example')

while True:
    # led.value() returns the current state of the LED
    # led.value(1) turns the LED on
    # led.value(0) turns the LED off
    led.value(not led.value())
    sleep(0.5)