import sh1106
import time
import framebuf
from machine import Pin, I2C

class Display:
    def __init__(self, i2c_bus=0, scl_pin=5, sda_pin=4, freq=400_000, x_size=128, y_size=64, rotate=0):
        self.i2c = I2C(i2c_bus, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
        self.display = sh1106.SH1106_I2C(x_size, y_size, self.i2c, res=None, addr=0x3c, rotate=rotate)
        self.display.sleep(False)
        self.display.fill(0)

    def show(self):
        self.display.show()

    def clear(self):
        self.display.fill(0)

    def animate_ball(self):
        ball_radius = 7
        x = 30
        y = 30
        dx = 2
        dy = 2

        while True:
            self.clear()
            # Draw the ball
            self.display.ellipse(x, y, ball_radius, ball_radius, 1, f=True) # type: ignore
            self.show()
            time.sleep_ms(1)

            # Update position
            x += dx
            y += dy

            # Bounce off the edges
            if x - ball_radius < 0 or x + ball_radius > 127:
                dx = -dx
            if y - ball_radius < 0 or y + ball_radius > 63:
                dy = -dy

    def draw_cat(self, x, y, width=64, height=64):
        # TODO: move thes byte array to a separate file?
        byte_array_cat = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 0, 0, 36, 0, 120, 0, 0, 0, 0, 0, 38, 1, 204, 0, 240, 0, 0, 0, 34, 3, 4, 1, 152, 0, 0, 0, 50, 6, 116, 3, 8, 0, 0, 0, 18, 12, 244, 6, 104, 0, 0, 0, 18, 25, 228, 12, 232, 0, 0, 0, 18, 19, 231, 249, 200, 0, 0, 0, 18, 16, 0, 0, 8, 0, 0, 0, 18, 240, 0, 0, 8, 0, 0, 0, 18, 128, 0, 0, 8, 0, 0, 0, 19, 128, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 6, 1, 136, 0, 0, 0, 16, 0, 9, 2, 72, 0, 0, 0, 48, 0, 9, 2, 72, 0, 0, 0, 32, 0, 9, 2, 72, 0, 0, 0, 32, 0, 0, 0, 8, 0, 0, 0, 32, 0, 0, 0, 8, 0, 0, 0, 32, 0, 0, 0, 24, 0, 0, 0, 32, 0, 0, 0, 16, 0, 0, 0, 32, 0, 0, 0, 16, 0, 0, 0, 32, 0, 0, 0, 112, 0, 0, 0, 96, 0, 0, 0, 64, 0, 0, 0, 67, 224, 127, 248, 64, 0, 0, 0, 70, 32, 64, 8, 96, 0, 0, 0, 68, 32, 64, 8, 32, 0, 0, 0, 68, 32, 192, 12, 32, 0, 0, 0, 76, 32, 128, 4, 48, 0, 0, 0, 120, 32, 128, 6, 16, 0, 0, 0, 0, 32, 128, 2, 16, 0, 0, 0, 0, 35, 128, 2, 16, 0, 0, 0, 0, 62, 0, 3, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # Create a frame buffer from the byte array
        fb = framebuf.FrameBuffer(byte_array_cat, width, height, framebuf.MONO_HLSB)
        # Blit the frame buffer onto the display at position (x, y)
        self.display.blit(fb, x, y, key=-1)
        self.show()

    def draw_weather(self, weather_data):
        self.clear()
        self.display.text_multiline(weather_data, 0, 0, 1)
        self.show()