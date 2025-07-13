import sh1106
from machine import Pin, I2C

def init_display(
    i2c_bus: int = 0,
    scl_pin: int = 5,
    sda_pin: int = 4,
    freq: int = 400_000,
    x_size: int = 128,
    y_size: int = 64,
    rotate: int = 0
) -> sh1106.SH1106_I2C:
    i2c = I2C(i2c_bus, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
    display = sh1106.SH1106_I2C(x_size, y_size, i2c, res=None, addr=0x3c, rotate=rotate)
    display.sleep(False)
    display.fill(0)
    return display