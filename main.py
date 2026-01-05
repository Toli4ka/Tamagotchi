import utime
from display import Display
from coffee_timer import CoffeeTimer
from wifi import init_wifi
from secrets import WIFI_SSID, WIFI_PASSWORD, CITY, DIRECTION
from weather import Weather
from buttons import Buttons
from vibro import VibroMotor
from micro_db import TrainFetcher

class Screen:
    MAIN = 1
    LEFT = 2
    RIGHT = 3
    MOOD_MENU = 4

class TamagotchiApp:
    def __init__(self):
        init_wifi(WIFI_SSID, WIFI_PASSWORD)
        self.display = Display(rotate=90)
        self.display.text("Loading", 4, 60, 1)
        self.display.text("...", 18, 70, 1)
        self.display.show()

        self.buttons = Buttons({'left': 20, 'middle': 19, 'right': 18})
        self.pressed_buttons = {} 
        self.vibro_motor = VibroMotor(pin_num=21)
        self.current_screen = Screen.MAIN

        self.weather_data = Weather(CITY).get_weather()
        if not self.weather_data: 
            print("Using default weather data")
            self.weather_data = {"temp": 0, "humidity": 0, "icon": "01d"}
    
        db = TrainFetcher()
        self.train_data = db.get_next_trains(2)

        self.timer_total_seconds = 120
        self.coffee_timer = CoffeeTimer(total_seconds=self.timer_total_seconds)
        self.coffee_timer_active = False
        self.coffee_anim_frame = 0
        self.last_anim_update = utime.ticks_ms() # rename

        self.animate_cat = False
        self.cat_anim_length = 0
        self.cat_anim_frame_idx = 0
        self.cat_anim_laset_update = utime.ticks_ms()

        self.mood_menu_active = False
        self.mood_score = 0
        self.display.draw_main_screen(mood_score=self.mood_score, weather_data=self.weather_data)

    def open_mood_menu(self):
        self.mood_menu_active = True
        self.display.task_selected_idx = 0
        self.display.draw_mood_menu(mood_score=self.mood_score)

    def screen_navigation_logic(self):
        # self.pressed_buttons = self.buttons.get_all_pressed()
        # LEFT SCREEN LOGIC
        if self.current_screen == Screen.LEFT:
            if self.pressed_buttons['right']:
                self.current_screen = Screen.MAIN
                self.display.draw_main_screen(mood_score=self.mood_score, weather_data=self.weather_data)
                self.vibro_motor.vibrate(100)
            # If left or middle pressed, do nothing (implement later)

        # MIDDLE SCREEN LOGIC
        elif self.current_screen == Screen.MAIN:
            if self.pressed_buttons['left']:
                self.current_screen = Screen.LEFT
                self.display.draw_left_screen(self.train_data)
                self.vibro_motor.vibrate(100)
            elif self.pressed_buttons['right']:
                self.current_screen = Screen.RIGHT
                self.display.draw_right_screen(self.coffee_timer)
                self.vibro_motor.vibrate(100)
            elif self.pressed_buttons['middle']:
                self.open_mood_menu()

        # RIGHT SCREEN LOGIC
        elif self.current_screen == Screen.RIGHT:
            if self.pressed_buttons['left']:
                self.current_screen = Screen.MAIN
                self.display.draw_main_screen(mood_score=self.mood_score, weather_data=self.weather_data)
                self.vibro_motor.vibrate(100)
            else:
                self.coffee_timer_logic()

    def coffee_timer_logic(self):
        # Timer finished
        if self.coffee_timer.seconds_left == 0:    
                    self.coffee_timer_active = False
                    # Reset timer
                    print("Coffee timer finished!")
                    self.coffee_timer.set_time(self.timer_total_seconds)
                    self.display.draw_right_screen(self.coffee_timer)
                    self.vibro_motor.vibrate(1000)

        # Handle timer option selection
        if self.pressed_buttons['middle']:
            if not self.coffee_timer.running:
                # Start timer
                print("START coffee timer")
                self.coffee_timer_active = True
                # self.coffee_timer.set_time(2, 0)
                self.coffee_timer.running = True
                self.vibro_motor.vibrate(200)

            else:
                # Stop timer if running
                self.coffee_timer.stop()
                print("STOP coffee timer")
                # Reset timer
                self.coffee_timer.set_time(self.timer_total_seconds)
                self.display.draw_right_screen(self.coffee_timer)
                self.coffee_timer_active = False
                self.vibro_motor.vibrate(200)

        elif self.pressed_buttons['right']:
            if not self.coffee_timer.running:
                # Select time for timer
                self.timer_total_seconds += 30
                if self.timer_total_seconds > 180:
                    self.timer_total_seconds = 30
                self.coffee_timer.set_time(self.timer_total_seconds)
                self.display.draw_right_screen(self.coffee_timer)
        
        elif self.pressed_buttons['left']:
            # Return to main screen
            self.coffee_timer_active = False
            self.coffee_timer.set_time(self.timer_total_seconds)
            # self.coffee_timer.running = False
            self.current_screen = Screen.MAIN
            self.display.draw_main_screen(mood_score=self.mood_score, weather_data=self.weather_data)

    def mood_menu_logic(self):
        # self.pressed_buttons = self.buttons.get_all_pressed()
        # Do not now how to implement this yet
        # if len(self.display.task_options) == 1:
        #     self.display.text("Time to", 0, 17, 1)
        #     self.display.text(" Relax", 0, 27, 1)
        #     # self.display.draw_cat(x=0, y=32, key=0)
        #     self.display.show()
        if self.pressed_buttons['left']:
            self.display.mood_menu_up()
            self.display.draw_mood_menu(mood_score=self.mood_score)
        elif self.pressed_buttons['right']:
            self.display.mood_menu_down()
            self.display.draw_mood_menu(mood_score=self.mood_score)
        elif self.pressed_buttons['middle']:
            selected_task = self.display.task_options[self.display.task_selected_idx]
            if selected_task != "EXIT":
                if self.mood_score < self.display.max_mood_score:
                    self.mood_score += 1
                    self.display.task_options.remove(selected_task)

                self.cat_anim_length = self.display.get_cat_anim_length(self.mood_score)
                self.cat_anim_last_update = utime.ticks_ms()
                self.cat_anim_frame_idx = 0 # start from first frame
                self.animate_cat = True
               
            self.mood_menu_active = False
            self.vibro_motor.vibrate(100)
            self.current_screen = Screen.MAIN
            # return to main screen without animation if EXIT was selected
            if selected_task == "EXIT":
                self.display.draw_main_screen(mood_score=self.mood_score, weather_data=self.weather_data)

    def _update_coffee_anim_frame(self, now):
        if self.coffee_timer.running and utime.ticks_diff(now, self.last_anim_update) > 150:
            self.coffee_anim_frame = (self.coffee_anim_frame + 1) % 6
            self.last_anim_update = now
            # To add a pause after a full loop
            if self.coffee_anim_frame == 0:
                self.last_anim_update += 500
        self.display.draw_right_screen(
                    self.coffee_timer, 
                    animate=self.coffee_timer.running,
                    animate_frame=self.coffee_anim_frame
                    )

    def _update_cat_anim_frame(self, now):
        if utime.ticks_diff(now, self.cat_anim_last_update) > 200:
            self.cat_anim_last_update = now
            self.display.draw_main_screen(
                mood_score=self.mood_score,
                frame_idx=self.cat_anim_frame_idx,
                animate=True,
                weather_data=self.weather_data
                )
            self.cat_anim_frame_idx += 1
            if self.cat_anim_frame_idx >= self.cat_anim_length:
                self.animate_cat = False
                self.display.draw_main_screen(mood_score=self.mood_score, weather_data=self.weather_data)

    def run(self):
        while True:
            now = utime.ticks_ms()
            self.pressed_buttons = self.buttons.get_all_pressed()

            # Cat Animation logic
            if self.animate_cat:
                self._update_cat_anim_frame(now)
                self.display.show()
                # TODO: find another way without continue
                continue # Skip other logic while animating

            # MOOD MENU LOGIC
            if self.mood_menu_active:
                self.mood_menu_logic()
                self.display.show()

            # COFFEE TIMER LOGIC
            elif self.coffee_timer_active:
                self._update_coffee_anim_frame(now) 
                self.coffee_timer_logic()
                self.coffee_timer.update()
                self.display.show()
            else:
                self.screen_navigation_logic()
                self.display.show()
            utime.sleep_ms(10)

if __name__ == "__main__":
    app = TamagotchiApp()
    import gc
    print("Used memory:", gc.mem_alloc(), "bytes")
    print("Free memory:", gc.mem_free(), "bytes")
    app.run()