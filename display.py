import sh1106
import utime
import framebuf
from machine import Pin, I2C
from pixel_art import coffee_cup_frames, cat1_frames, cat2_frames, cat3_frames, cat4_frames, cat5_frames, cats, nav_arrow_down, nav_arrow_up, nav_arrow_left, nav_arrow_right, nav_middle, nav_play, nav_stop, nav_watch, weather_broken_clouds, weather_clear_sky, weather_few_clouds, weather_mist, weather_rain, weather_scattered_clouds, weather_shower_rain, weather_snow, weather_thunderstorm

class Display:
    def __init__(self, i2c_bus=0, scl_pin=5, sda_pin=4, freq=400_000, x_size=128, y_size=64, rotate=0):
        self.i2c = I2C(i2c_bus, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
        self.display = sh1106.SH1106_I2C(x_size, y_size, self.i2c, res=None, addr=0x3c, rotate=rotate)
        self.display.sleep(False)
        self.display.fill(0)

        self.task_options = ["Water", "Walk", "Book", "Yoga", "Sketch", "EXIT"]
        self.max_mood_score = len(self.task_options) - 1
        self.task_selected_idx = 0
        self.mood_window_start = 0
        self.mood_window_size = 3

        self.coffee_timer_seconds = 0
        self.coffee_timer_running = False
        self.last_coffee_timer_update = utime.ticks_ms()


    def show(self):
        self.display.show()

    def clear(self):
        self.display.fill(0)

    def text(self, string, x, y, color=1):
        self.display.text(string, x, y, color)

    def draw_coffee_cup(self, x, y, width=64, height=64, key=-1):
        # # Flattened (x, y) pairs as bytes
        # pixel_array_coffee_cup = bytearray([
        #     17, 7, 18, 7, 19, 7, 20, 7, 21, 7, 22, 7, 23, 7, 24, 7, 25, 7, 26, 7, 27, 7, 28, 7, 29, 7, 30, 7, 31, 7, 32, 7, 33, 7, 34, 7, 35, 7, 36, 7, 37, 7, 38, 7, 39, 7, 40, 7, 41, 7, 42, 7, 43, 7, 44, 7, 45, 7, 46, 7, 16, 8, 20, 8, 25, 8, 31, 8, 37, 8, 42, 8, 47, 8, 16, 9, 17, 9, 21, 9, 25, 9, 31, 9, 37, 9, 41, 9, 46, 9, 47, 9, 17, 10, 21, 10, 26, 10, 31, 10, 36, 10, 41, 10, 46, 10, 18, 11, 21, 11, 26, 11, 31, 11, 36, 11, 40, 11, 41, 11, 45, 11, 18, 12, 20, 12, 21, 12, 22, 12, 24, 12, 25, 12, 26, 12, 29, 12, 30, 12, 31, 12, 33, 12, 34, 12, 35, 12, 36, 12, 38, 12, 39, 12, 40, 12, 42, 12, 43, 12, 44, 12, 45, 12, 19, 13, 21, 13, 22, 13, 25, 13, 26, 13, 27, 13, 29, 13, 30, 13, 31, 13, 33, 13, 34, 13, 35, 13, 36, 13, 38, 13, 39, 13, 40, 13, 42, 13, 43, 13, 44, 13, 19, 14, 22, 14, 23, 14, 26, 14, 27, 14, 29, 14, 30, 14, 31, 14, 33, 14, 34, 14, 35, 14, 38, 14, 39, 14, 42, 14, 43, 14, 44, 14, 20, 15, 23, 15, 26, 15, 27, 15, 29, 15, 30, 15, 31, 15, 33, 15, 34, 15, 35, 15, 38, 15, 39, 15, 41, 15, 42, 15, 43, 15, 20, 16, 21, 16, 23, 16, 24, 16, 26, 16, 27, 16, 29, 16, 30, 16, 31, 16, 33, 16, 34, 16, 35, 16, 37, 16, 38, 16, 39, 16, 41, 16, 42, 16, 43, 16, 21, 17, 24, 17, 27, 17, 30, 17, 31, 17, 33, 17, 34, 17, 35, 17, 37, 17, 38, 17, 40, 17, 41, 17, 42, 17, 21, 18, 22, 18, 24, 18, 25, 18, 27, 18, 28, 18, 30, 18, 31, 18, 33, 18, 34, 18, 37, 18, 38, 18, 40, 18, 41, 18, 42, 18, 22, 19, 25, 19, 27, 19, 28, 19, 31, 19, 33, 19, 34, 19, 37, 19, 40, 19, 41, 19, 23, 20, 25, 20, 26, 20, 28, 20, 29, 20, 31, 20, 33, 20, 34, 20, 36, 20, 37, 20, 39, 20, 40, 20, 23, 21, 26, 21, 29, 21, 31, 21, 33, 21, 34, 21, 36, 21, 39, 21, 40, 21, 24, 22, 26, 22, 27, 22, 29, 22, 31, 22, 33, 22, 34, 22, 36, 22, 38, 22, 39, 22, 24, 23, 25, 23, 27, 23, 29, 23, 31, 23, 33, 23, 35, 23, 37, 23, 38, 23, 39, 23, 25, 24, 27, 24, 29, 24, 31, 24, 33, 24, 35, 24, 37, 24, 38, 24, 16, 25, 17, 25, 18, 25, 19, 25, 20, 25, 21, 25, 22, 25, 23, 25, 24, 25, 25, 25, 26, 25, 27, 25, 28, 25, 29, 25, 30, 25, 31, 25, 32, 25, 33, 25, 34, 25, 35, 25, 36, 25, 37, 25, 38, 25, 39, 25, 40, 25, 41, 25, 42, 25, 43, 25, 44, 25, 45, 25, 46, 25, 47, 25, 16, 26, 17, 26, 18, 26, 19, 26, 20, 26, 21, 26, 22, 26, 23, 26, 24, 26, 25, 26, 26, 26, 27, 26, 28, 26, 29, 26, 30, 26, 31, 26, 32, 26, 33, 26, 34, 26, 35, 26, 36, 26, 37, 26, 38, 26, 39, 26, 40, 26, 41, 26, 42, 26, 43, 26, 44, 26, 45, 26, 46, 26, 47, 26, 21, 27, 26, 27, 37, 27, 43, 27, 19, 28, 20, 28, 27, 28, 28, 28, 29, 28, 30, 28, 31, 28, 32, 28, 33, 28, 34, 28, 35, 28, 36, 28, 43, 28, 20, 29, 21, 29, 42, 29, 21, 30, 41, 30, 42, 30, 43, 30, 44, 30, 45, 30, 46, 30, 47, 30, 48, 30, 22, 31, 48, 31, 49, 31, 23, 32, 41, 32, 42, 32, 43, 32, 44, 32, 45, 32, 46, 32, 49, 32, 50, 32, 23, 33, 40, 33, 46, 33, 47, 33, 50, 33, 23, 34, 40, 34, 47, 34, 48, 34, 50, 34, 21, 35, 22, 35, 41, 35, 42, 35, 48, 35, 50, 35, 21, 36, 42, 36, 48, 36, 50, 36, 21, 37, 42, 37, 48, 37, 50, 37, 21, 38, 22, 38, 35, 38, 36, 38, 37, 38, 38, 38, 39, 38, 41, 38, 42, 38, 48, 38, 50, 38, 20, 39, 43, 39, 48, 39, 50, 39, 20, 40, 43, 40, 48, 40, 50, 40, 19, 41, 20, 41, 21, 41, 37, 41, 38, 41, 39, 41, 40, 41, 42, 41, 43, 41, 44, 41, 48, 41, 50, 41, 19, 42, 44, 42, 47, 42, 50, 42, 19, 43, 44, 43, 45, 43, 46, 43, 49, 43, 50, 43, 19, 44, 20, 44, 39, 44, 40, 44, 41, 44, 42, 44, 43, 44, 48, 44, 49, 44, 18, 45, 45, 45, 46, 45, 47, 45, 48, 45, 18, 46, 45, 46, 18, 47, 45, 47, 17, 48, 18, 48, 19, 48, 20, 48, 21, 48, 22, 48, 23, 48, 24, 48, 25, 48, 26, 48, 27, 48, 28, 48, 29, 48, 30, 48, 31, 48, 32, 48, 33, 48, 34, 48, 35, 48, 36, 48, 37, 48, 38, 48, 39, 48, 40, 48, 41, 48, 42, 48, 43, 48, 44, 48, 45, 48, 46, 48, 17, 49, 18, 49, 19, 49, 20, 49, 21, 49, 22, 49, 23, 49, 24, 49, 25, 49, 26, 49, 27, 49, 28, 49, 29, 49, 30, 49, 31, 49, 32, 49, 33, 49, 34, 49, 35, 49, 36, 49, 37, 49, 38, 49, 39, 49, 40, 49, 41, 49, 42, 49, 43, 49, 44, 49, 45, 49, 46, 49, 17, 50, 18, 50, 19, 50, 20, 50, 21, 50, 22, 50, 23, 50, 24, 50, 25, 50, 26, 50, 27, 50, 28, 50, 29, 50, 30, 50, 31, 50, 32, 50, 33, 50, 34, 50, 35, 50, 36, 50, 37, 50, 38, 50, 39, 50, 40, 50, 41, 50, 42, 50, 43, 50, 44, 50, 45, 50, 46, 50, 17, 51, 18, 51, 19, 51, 20, 51, 21, 51, 22, 51, 23, 51, 24, 51, 25, 51, 26, 51, 27, 51, 28, 51, 29, 51, 30, 51, 31, 51, 32, 51, 33, 51, 34, 51, 35, 51, 36, 51, 37, 51, 38, 51, 39, 51, 40, 51, 41, 51, 42, 51, 43, 51, 44, 51, 45, 51, 46, 51, 18, 52, 19, 52, 20, 52, 21, 52, 22, 52, 23, 52, 24, 52, 25, 52, 26, 52, 27, 52, 28, 52, 29, 52, 30, 52, 31, 52, 32, 52, 33, 52, 34, 52, 35, 52, 36, 52, 37, 52, 38, 52, 39, 52, 40, 52, 41, 52, 42, 52, 43, 52, 44, 52, 45, 52, 19, 53, 20, 53, 21, 53, 22, 53, 23, 53, 24, 53, 25, 53, 26, 53, 27, 53, 28, 53, 29, 53, 30, 53, 31, 53, 32, 53, 33, 53, 34, 53, 35, 53, 36, 53, 37, 53, 38, 53, 39, 53, 40, 53, 41, 53, 42, 53, 43, 53, 44, 53
        # ])
        # for i in range(0, len(pixel_array_coffee_cup), 2):
        #     xx = pixel_array_coffee_cup[i]
        #     yy = pixel_array_coffee_cup[i + 1]
        #     self.display.pixel(x + xx, y + yy, 1)
        fb = framebuf.FrameBuffer(coffee_cup_frames[0], width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, x, y, key=key)

    def draw_coffee_cup_frame(self, x, y, frame_idx, width=64, height=64, key=-1):
        fb = framebuf.FrameBuffer(coffee_cup_frames[frame_idx], width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, x, y, key=key)

    def draw_cat_from_array(self, x, y, mood_score=0, width=64, height=64, key=-1):
        fb = framebuf.FrameBuffer(cats[mood_score], width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, x, y, key=key)

    def get_cat_anim_length(self, mood_score):
        if mood_score == 1:
            return len(cat1_frames)
        elif mood_score == 2:
            return len(cat2_frames)
        elif mood_score == 3:
            return len(cat3_frames)
        elif mood_score == 4:
            return len(cat4_frames)
        elif mood_score == 5:
            return len(cat5_frames)
        return 1

    def draw_cat_frame(self, x, y, mood_score, frame_idx, width=64, height=64, key=-1):
        if mood_score == 1:
            frames = cat1_frames
        elif mood_score == 2:
            frames = cat2_frames
        elif mood_score == 3:
            frames = cat3_frames
        elif mood_score == 4:
            frames = cat4_frames
        elif mood_score == 5:
            frames = cat5_frames

        fb = framebuf.FrameBuffer(frames[frame_idx], width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, x, y, key=key)

    def _draw_weather_icon(self, icon, x=45, y=0, width=16, height=16, key=-1):
        if icon == "01d" or icon == "01n":  # clear sky day/night
            weather_icon = weather_clear_sky
        elif icon == "02d" or icon == "02n":  # few clouds
            weather_icon = weather_few_clouds
        elif icon == "03d" or icon == "03n":  # scattered clouds
            weather_icon = weather_scattered_clouds
        elif icon == "04d" or icon == "04n":  # broken clouds
            weather_icon = weather_broken_clouds
        elif icon == "09d" or icon == "09n":  # shower rain
            weather_icon = weather_shower_rain
        elif icon == "10d" or icon == "10n":  # rain
            weather_icon = weather_rain
        elif icon == "11d" or icon == "11n":  # thunderstorm
            weather_icon = weather_thunderstorm
        elif icon == "13d" or icon == "13n":  # snow
            weather_icon = weather_snow
        elif icon == "50d" or icon == "50n":  # mist
            weather_icon = weather_mist
        else:
            return  # Unknown icon
        fb = framebuf.FrameBuffer(weather_icon, width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, x, y, key=key)

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
        self.display.fill_rect(x_0 + 11, y_0 + 1, int(50 * mood_score/self.max_mood_score), 6, 1)
        # draw the bound of the scale
        self._draw_mood_scale_bound(x_0, y_0)
       

    def draw_weather(self, weather_data):
        if weather_data:
            temp = weather_data["temp"]
            humidity = weather_data["humidity"]
            icon = weather_data["icon"]
            self.display.text(f"T:{temp}C", 0, 0, 1)
            self.display.text(f"H:{humidity}%", 0, 10, 1)
            # print(f"Weather: {temp}C, {humidity}%, {icon}")
            self._draw_weather_icon(icon)

        else:
            self.display.text("No data", 0, 0, 1)

    def draw_navigation(self, width=8, height=8 , key=-1):
        # Draw navigation arrows
        fb = framebuf.FrameBuffer(nav_arrow_left, width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, 0, 118, key=key)

        fb = framebuf.FrameBuffer(nav_middle, width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, 28, 118, key=key)

        fb = framebuf.FrameBuffer(nav_arrow_right, width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, 56, 118, key=key)

    def draw_coffee_navigation(self, animate=False, width=8, height=8, key=-1):
        # Draw coffee navigation arrows
        
        fb = framebuf.FrameBuffer(nav_arrow_left, width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, 0, 118, key=key)
        
        fb = framebuf.FrameBuffer(nav_play, width, height, framebuf.MONO_HLSB)
        if animate:
            fb = framebuf.FrameBuffer(nav_stop, width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, 28, 118, key=key)

        fb = framebuf.FrameBuffer(nav_watch, width, height, framebuf.MONO_HLSB)
        if not animate:
            self.display.blit(fb, 56, 118, key=key)

    def draw_mood_menu_navigation(self, width=8, height=8):
        # Draw mood menu navigation arrows
        fb = framebuf.FrameBuffer(nav_arrow_up, width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, 0, 118, key=-1)

        self.display.text('OK', 24, 118, 1)  # OK button for selection

        fb = framebuf.FrameBuffer(nav_arrow_down, width, height, framebuf.MONO_HLSB)
        self.display.blit(fb, 56, 118, key=-1)

    def draw_mood_menu(self, mood_score):
        # Draw part of the main screen with mood menu navigation buttons
        self.clear()
        self.draw_cat_from_array(0, 36, mood_score=mood_score)
        self.draw_mood_scale(x_0=1, y_0=100, mood_score=mood_score)
        self.draw_mood_menu_navigation()
        
        # self.draw_main_screen(mood_score=mood_score, cat_x=0, cat_y=36, draw_weather=False, mood_menu_navigation=True)

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
        self.display.rect(x0, y0, menu_width, menu_height, 1)
        # draw just the button line
        # self.display.hline(x0+4, y0 + menu_height+4, menu_width-2*4, 1)
        # self.show()

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

    def draw_main_screen(self, mood_score, weather_data, cat_x=0, cat_y=36, animate=False, frame_idx=0):
        self.clear()
        # Draw the main screen elements here
        if weather_data:
            self.draw_weather(weather_data)

        if animate:
            # We need to draw here one frame at a time. Not the whole animation 
            self.draw_cat_frame(cat_x, cat_y, mood_score=mood_score, frame_idx=frame_idx)
        else:
            self.draw_cat_from_array(cat_x, cat_y, mood_score=mood_score)
        
        self.draw_mood_scale(x_0=1, y_0=100, mood_score=mood_score)
        self.draw_navigation()

    def draw_right_screen(self, coffee_timer, animate=False, animate_frame=0):
        self.clear()
        self.display.text("COFFEE", 8, 4, 1)
        self.display.rect(0, 16, 64, 16, 1)

        self.text(coffee_timer.get_time(), 14, 20, 1)

        if animate:
            self.draw_coffee_cup_frame(x=0, y=46, frame_idx=animate_frame)
        else:
            self.draw_coffee_cup(x=0, y=46)

        self.draw_coffee_navigation(animate=animate)

    def draw_left_screen(self):
        self.clear()
        self.display.text("TEST", 0, 0, 1)
        self._draw_weather_icon(x=0, y=20, icon="01d")
        self._draw_weather_icon(x=20, y=20, icon="02d")
        self._draw_weather_icon(x=40, y=20, icon="03d")
        self._draw_weather_icon(x=0, y=40, icon="04d")
        self._draw_weather_icon(x=20, y=40, icon="09d")
        self._draw_weather_icon(x=40, y=40, icon="10d")
        self._draw_weather_icon(x=0, y=60, icon="11d")
        self._draw_weather_icon(x=20, y=60, icon="13d")
        self._draw_weather_icon(x=40, y=60, icon="50d")
        width = 8
        height = 8

        self.draw_navigation()

# implement timer
class CoffeeTimer:
    def __init__(self, total_seconds=0):
        self.running = False
        self.total_seconds = total_seconds
        self.seconds_left = total_seconds
        self.last_update = utime.ticks_ms()

    def set_time(self, total_seconds):
        self.total_seconds = total_seconds
        self.seconds_left = self.total_seconds

    def update(self):
        if self.running:
            now = utime.ticks_ms()
            if utime.ticks_diff(now, self.last_update) >= 1000:
                if self.seconds_left > 0:
                    self.seconds_left -= 1
                    self.last_update = now
                else:
                    self.running = False

    def stop(self):
        self.running = False
        self.seconds_left = self.total_seconds

    def get_time(self):
        return f"{self.seconds_left // 60:02}:{self.seconds_left % 60:02}"