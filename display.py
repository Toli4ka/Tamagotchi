import sh1106
import time
import framebuf
from machine import Pin, I2C
from weather import Weather

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

    def draw_cat(self, x, y, width=64, height=64):
        # TODO: move thes byte array to a separate file?
        byte_array_cat = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 0, 0, 36, 0, 120, 0, 0, 0, 0, 0, 38, 1, 204, 0, 240, 0, 0, 0, 34, 3, 4, 1, 152, 0, 0, 0, 50, 6, 116, 3, 8, 0, 0, 0, 18, 12, 244, 6, 104, 0, 0, 0, 18, 25, 228, 12, 232, 0, 0, 0, 18, 19, 231, 249, 200, 0, 0, 0, 18, 16, 0, 0, 8, 0, 0, 0, 18, 240, 0, 0, 8, 0, 0, 0, 18, 128, 0, 0, 8, 0, 0, 0, 19, 128, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 6, 1, 136, 0, 0, 0, 16, 0, 9, 2, 72, 0, 0, 0, 48, 0, 9, 2, 72, 0, 0, 0, 32, 0, 9, 2, 72, 0, 0, 0, 32, 0, 0, 0, 8, 0, 0, 0, 32, 0, 0, 0, 8, 0, 0, 0, 32, 0, 0, 0, 24, 0, 0, 0, 32, 0, 0, 0, 16, 0, 0, 0, 32, 0, 0, 0, 16, 0, 0, 0, 32, 0, 0, 0, 112, 0, 0, 0, 96, 0, 0, 0, 64, 0, 0, 0, 67, 224, 127, 248, 64, 0, 0, 0, 70, 32, 64, 8, 96, 0, 0, 0, 68, 32, 64, 8, 32, 0, 0, 0, 68, 32, 192, 12, 32, 0, 0, 0, 76, 32, 128, 4, 48, 0, 0, 0, 120, 32, 128, 6, 16, 0, 0, 0, 0, 32, 128, 2, 16, 0, 0, 0, 0, 35, 128, 2, 16, 0, 0, 0, 0, 62, 0, 3, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # Create a frame buffer from the byte array
        fb = framebuf.FrameBuffer(byte_array_cat, width, height, framebuf.MONO_HLSB)
        # Blit the frame buffer onto the display at position (x, y)
        self.display.blit(fb, x, y, key=-1)

    def draw_sun(self, x, y):
        self.display.ellipse(x+7, y+7, 4, 4, 1, f=False) # type: ignore

        # Rays (4 sides)
        self.display.fill_rect(x+6, y, 3, 2, 1)        # Top
        self.display.fill_rect(x+6, y+13, 3, 2, 1)     # Bottom
        self.display.fill_rect(x, y+6, 2, 3, 1)        # Left
        self.display.fill_rect(x+13, y+6, 2, 3, 1)     # Right

        # Diagonal rays (corners)
        self.display.fill_rect(x+1, y+1, 2, 2, 1)      # Top-left
        self.display.fill_rect(x+12, y+1, 2, 2, 1)     # Top-right
        self.display.fill_rect(x+1, y+12, 2, 2, 1)     # Bottom-left
        self.display.fill_rect(x+12, y+12, 2, 2, 1)    # Bottom-right

    def draw_cloud(self, x, y):
        # Outline
        # Bottom
        y = y - 3
        self.display.hline(x+2, y+13, 12, 1)
        self.display.pixel(x+1, y+12, 1)
        self.display.pixel(x+14, y+12, 1)
        self.display.pixel(x+15, y+11, 1)

        # Lower left puff
        self.display.pixel(x+1, y+11, 1)
        self.display.pixel(x+1, y+10, 1)
        self.display.pixel(x+2, y+9, 1)
        self.display.hline(x+3, y+8, 2, 1)
        self.display.pixel(x+4, y+7, 1)

        # Left-middle puff
        self.display.hline(x+5, y+6, 3, 1)
        self.display.pixel(x+4, y+7, 1)
        self.display.pixel(x+8, y+6, 1)

        # Top bump
        self.display.hline(x+8, y+5, 4, 1)
        self.display.pixel(x+7, y+6, 1)
        self.display.pixel(x+12, y+6, 1)

        # Right bump
        self.display.hline(x+12, y+7, 3, 1)
        self.display.pixel(x+15, y+8, 1)
        self.display.pixel(x+15, y+9, 1)
        self.display.pixel(x+15, y+10, 1)
        self.display.pixel(x+15, y+11, 1)

    def draw_rain(self, x, y):
        self.draw_cloud(x, y-2)
        # Draw raindrops
        for i in range(3):
            self.display.line(x+4+4*i, y+11, x+2+4*i, y+13, 1)

    def draw_snowflake(self, x, y):
        # This draws an 8x8 snowflake, with center at (x+4, y+4)
        # Center "hole"
        self.display.pixel(x+4, y+4, 0)
        # Main arms (up, down, left, right, 2 pixels each)
        self.display.pixel(x+4, y+2, 1)
        self.display.pixel(x+4, y+1, 1)
        self.display.pixel(x+4, y+6, 1)
        self.display.pixel(x+4, y+7, 1)
        self.display.pixel(x+2, y+4, 1)
        self.display.pixel(x+1, y+4, 1)
        self.display.pixel(x+6, y+4, 1)
        self.display.pixel(x+7, y+4, 1)
        # Diagonal arms (make a 6-armed snowflake)
        self.display.pixel(x+2, y+2, 1)
        self.display.pixel(x+1, y+1, 1)
        self.display.pixel(x+6, y+6, 1)
        self.display.pixel(x+7, y+7, 1)
        self.display.pixel(x+6, y+2, 1)
        self.display.pixel(x+7, y+1, 1)
        self.display.pixel(x+2, y+6, 1)
        self.display.pixel(x+1, y+7, 1)

        # Tips (make them a bit thicker for a stylized look)
        # Vertical
        self.display.pixel(x+8, y+3, 1)
        self.display.pixel(x+8, y+12, 1)
        # Horizontal
        self.display.pixel(x+3, y+8, 1)
        self.display.pixel(x+12, y+8, 1)
        # Diagonal /
        self.display.pixel(x+3, y+3, 1)
        self.display.pixel(x+13, y+13, 1)
        # Diagonal \
        self.display.pixel(x+13, y+3, 1)
        self.display.pixel(x+3, y+13, 1)

    def _draw_weather_icon(self, desc):
        x = 45
        y = 0
        if desc == "Cloudy":
            self.draw_cloud(x, y)
        elif desc == "Sunny":
            self.draw_sun(x, y)
        elif desc == "Rainy":
            self.draw_rain(x, y)
        elif desc == "Snowy":
            self.draw_snowflake(x, y)
        else:
            self.draw_cloud(x, y)

    def draw_weather(self, weather_data):
        if weather_data:
            temp = weather_data["temp"]
            humidity = weather_data["humidity"]
            desc = weather_data["desc"]
            self.display.text(f"T:{temp}C", 0, 0, 1)
            self.display.text(f"H:{humidity}%", 0, 10, 1)
            self._draw_weather_icon(desc)
        else:
            self.display.text("No data", 0, 0, 1)

    def draw_smiley_face(self):
        # Center coordinates and radius for the face
        center_x = 64
        center_y = 32
        radius = 30

        # Face outline
        self.display.ellipse(center_x, center_y, radius, radius, 1, f=False) # type: ignore

        # Eyes
        self.display.fill_rect(center_x - 10, center_y - 10, 6, 6, 1)   # Left eye
        self.display.fill_rect(center_x + 10, center_y - 10, 6, 6, 1)   # Right eye

        # Smile (drawn as an arc using lines)
        for x in range(-13, 14):
            y = int(10 * ((1 - (x/13)**2)**0.5))
            self.display.pixel(center_x + x, center_y + 8 + y, 1)

        self.show()

    def draw_main_screen(self):
        self.clear()
        # Draw the main screen elements here
        self.draw_weather(Weather("Munich").get_weather())
        self.draw_cat(0, 36)
        self.show()