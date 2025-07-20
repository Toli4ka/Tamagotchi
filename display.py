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

        self.task_options = ["Water", "Walk", "Book", "Yoga", "Nap", "Snack", "Music", "EXIT"]
        self.task_selected_idx = 0
        self.mood_window_start = 0
        self.mood_window_size = 3

    def show(self):
        self.display.show()

    def clear(self):
        self.display.fill(0)

    def text(self, string, x, y, color=1):
        self.display.text(string, x, y, color)

    def draw_cat(self, x, y, width=64, height=64, key=-1):
        # TODO: move thes byte array to a separate file?
        byte_array_cat = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 36, 0, 0, 0, 0, 0, 0, 0, 36, 0, 120, 0, 0, 0, 0, 0, 38, 1, 204, 0, 240, 0, 0, 0, 34, 3, 4, 1, 152, 0, 0, 0, 50, 6, 116, 3, 8, 0, 0, 0, 18, 12, 244, 6, 104, 0, 0, 0, 18, 25, 228, 12, 232, 0, 0, 0, 18, 19, 231, 249, 200, 0, 0, 0, 18, 16, 0, 0, 8, 0, 0, 0, 18, 240, 0, 0, 8, 0, 0, 0, 18, 128, 0, 0, 8, 0, 0, 0, 19, 128, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 8, 0, 0, 0, 16, 0, 6, 1, 136, 0, 0, 0, 16, 0, 9, 2, 72, 0, 0, 0, 48, 0, 9, 2, 72, 0, 0, 0, 32, 0, 9, 2, 72, 0, 0, 0, 32, 0, 0, 0, 8, 0, 0, 0, 32, 0, 0, 0, 8, 0, 0, 0, 32, 0, 0, 0, 24, 0, 0, 0, 32, 0, 0, 0, 16, 0, 0, 0, 32, 0, 0, 0, 16, 0, 0, 0, 32, 0, 0, 0, 112, 0, 0, 0, 96, 0, 0, 0, 64, 0, 0, 0, 67, 224, 127, 248, 64, 0, 0, 0, 70, 32, 64, 8, 96, 0, 0, 0, 68, 32, 64, 8, 32, 0, 0, 0, 68, 32, 192, 12, 32, 0, 0, 0, 76, 32, 128, 4, 48, 0, 0, 0, 120, 32, 128, 6, 16, 0, 0, 0, 0, 32, 128, 2, 16, 0, 0, 0, 0, 35, 128, 2, 16, 0, 0, 0, 0, 62, 0, 3, 240, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # Create a frame buffer from the byte array
        fb = framebuf.FrameBuffer(byte_array_cat, width, height, framebuf.MONO_HLSB)
        # Blit the frame buffer onto the display at position (x, y)
        self.display.blit(fb, x, y, key=key)

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

    def _draw_mood_heart(self, x_0, y_0):
        black_pixels = [
            (1,1),(2,1),(5,1),(6,1),
            (0,2),(3,2),(4,2),(7,2),
            (0,3),(7,3),
            (1,4),(6,4),
            (2,5),(5,5),
            (3,6),(4,6)
        ]

        for x, y in black_pixels:
            self.display.pixel(x_0 + x, y_0 + y, 1)

    def _draw_mood_scale_bound(self, x_0, y_0):
        x_0_scale = 10
        x_scale = 52
        y_scale = 6

        self.display.hline(x_0+x_0_scale, y_0+1, x_scale, 1)
        self.display.hline(x_0+x_0_scale, y_0+y_scale, x_scale, 1)
        self.display.vline(x_0+x_0_scale, y_0+1, y_scale, 1)
        self.display.vline(x_0+x_0_scale+x_scale-1, y_0+1, y_scale, 1)

        # # Fill edge pixels
        self.display.pixel(x_0+x_0_scale, y_0+1, 0)
        self.display.pixel(x_0+x_0_scale, y_0+2, 0)
        self.display.pixel(x_0+x_0_scale, y_0+5, 0)
        self.display.pixel(x_0+x_0_scale, y_0+6, 0)
        self.display.pixel(x_0+x_0_scale+1, y_0+1, 0)
        self.display.pixel(x_0+x_0_scale+1, y_0+6, 0)
        self.display.pixel(x_0+x_0_scale+1, y_0+2, 1)
        self.display.pixel(x_0+x_0_scale+1, y_0+5, 1)

        self.display.pixel(x_0+x_0_scale+x_scale-1, y_0+1, 0)
        self.display.pixel(x_0+x_0_scale+x_scale-1, y_0+2, 0)
        self.display.pixel(x_0+x_0_scale+x_scale-1, y_0+5, 0)
        self.display.pixel(x_0+x_0_scale+x_scale-1, y_0+6, 0)
        self.display.pixel(x_0+x_0_scale+x_scale-1-1, y_0+1, 0)
        self.display.pixel(x_0+x_0_scale+x_scale-1-1, y_0+6, 0)
        self.display.pixel(x_0+x_0_scale+x_scale-1-1, y_0+2, 1)
        self.display.pixel(x_0+x_0_scale+x_scale-1-1, y_0+5, 1)

    def draw_mood_scale(self, x_0, y_0, mood_score):
        self._draw_mood_heart(x_0, y_0)
        # then fill the scale n * mood_score
        self.display.fill_rect(x_0 + 11, y_0 + 1, mood_score * 10, 6, 1)
        # draw the bound of the scale
        self._draw_mood_scale_bound(x_0, y_0)
       


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

    def draw_navigation(self):
        # Draw navigation arrows
        self.display.text('<', 0, 118, 1)  
        self.display.text('[', 24, 118, 1)
        self.display.text(']', 32, 118, 1)
        self.display.text('>', 56, 118, 1)  

    def draw_mood_menu(self):
        options = self.task_options
        selected_idx = self.task_selected_idx
        window_start = self.mood_window_start
        window_size = self.mood_window_size

        # Adjust window start if needed
        if selected_idx < window_start:
            window_start = selected_idx
        elif selected_idx >= window_start + window_size:
            window_start = selected_idx - window_size + 1
        self.mood_window_start = window_start

        # Draw overlay in the center
        menu_height = 34
        menu_width = 64
        # try to place on top
        x0 = 0
        y0 = 0
        # x0 = 0
        # y0 = 64
        self.display.fill_rect(x0, y0, menu_width, menu_height, 0)
        # self.display.rect(x0, y0, menu_width, menu_height, 1)
        # draw just the button line
        self.display.hline(x0+4, y0 + menu_height+4, menu_width-2*4, 1)

        y = y0 + 4
        for i in range(window_start, min(window_start + window_size, len(options))):
            prefix = ">" if i == selected_idx else " "
            self.display.text(prefix + options[i], x0 + 6, y)
            y += 10

    def mood_menu_up(self):
        # Wrap to last if at first
        if self.task_selected_idx == 0:
            self.task_selected_idx = len(self.task_options) - 1
        else:
            self.task_selected_idx -= 1

    def mood_menu_down(self):
        # Wrap to first if at last
        if self.task_selected_idx == len(self.task_options) - 1:
            self.task_selected_idx = 0
        else:
            self.task_selected_idx += 1

    def draw_main_screen(self, mood_score=0, cat_x=0, cat_y=32):
        self.clear()
        # Draw the main screen elements here
        self.draw_weather(Weather("Munich").get_weather())
        # self.display.text('TESTTEST', 0, 0, 1)  
        # self.display.text('TESTTEST', 0, 10, 1) 
        self.draw_cat(cat_x, cat_y)
        self.draw_navigation()
        self.draw_mood_scale(x_0=1, y_0=100, mood_score=mood_score)  # Example mood score
        # self.show()