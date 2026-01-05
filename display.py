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

    def draw_train_info(self, train_data, x_start=0, y_start=0):
        if not train_data or len(train_data) == 0:
            self.display.text("No train data", x_start, y_start, 1)
            return

        # Show up to two trains, each on its own line
        for idx, train in enumerate(train_data[:2]):
            time = train.get("actual_time", "--:--")
            platform = train.get("platform", "?")
            # # for debug set cancelled to True for the first train
            # if idx == 0:
            #     train["cancelled"] = True
            if train.get("cancelled", False):
                self.display.text(f"{time} P{platform}", x_start, y_start + 10 * idx, 1)
                self.display.hline(x_start, y_start + 10 * idx + 3, 64, 1)
            else:
                self.display.text(f"{time}|P{platform}", x_start, y_start + 10 * idx, 1)

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

    def draw_left_screen(self, train_data):
        self.clear()
        # self.display.text("TEST", 0, 0, 1)
        # self._draw_weather_icon(x=0, y=20, icon="01d")
        # self._draw_weather_icon(x=20, y=20, icon="02d")
        # self._draw_weather_icon(x=40, y=20, icon="03d")
        # self._draw_weather_icon(x=0, y=40, icon="04d")
        # self._draw_weather_icon(x=20, y=40, icon="09d")
        # self._draw_weather_icon(x=40, y=40, icon="10d")
        # self._draw_weather_icon(x=0, y=60, icon="11d")
        # self._draw_weather_icon(x=20, y=60, icon="13d")
        # self._draw_weather_icon(x=40, y=60, icon="50d")
        x_text_start = 24
        y_text_start = 4
        self.display.text("S5", x_text_start, y_text_start, 1)
        # self.display.ellipse(32, 8, 20, 10, 1)
        self.display.rect(x_text_start-4, y_text_start-4, 16+4*2, 8+4*2, 1)
        if train_data:
            self.draw_train_info(train_data, x_start=0, y_start=20)
        else:
            self.display.text("No data", 0, 30, 1)


        self.draw_navigation()

# implement timer
# class CoffeeTimer:
#     def __init__(self, total_seconds=0):
#         self.running = False
#         self.total_seconds = total_seconds
#         self.seconds_left = total_seconds
#         self.last_update = utime.ticks_ms()

#     def set_time(self, total_seconds):
#         self.total_seconds = total_seconds
#         self.seconds_left = self.total_seconds

#     def update(self):
#         if self.running:
#             now = utime.ticks_ms()
#             if utime.ticks_diff(now, self.last_update) >= 1000:
#                 if self.seconds_left > 0:
#                     self.seconds_left -= 1
#                     self.last_update = now
#                 else:
#                     self.running = False
                    
#     def stop(self):
#         self.running = False
#         self.seconds_left = self.total_seconds

#     def get_time(self):
#         return f"{self.seconds_left // 60:02}:{self.seconds_left % 60:02}"