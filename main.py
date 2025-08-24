from machine import Pin
import utime
from display import Display, CoffeeTimer
from wifi import init_wifi
from secrets import WIFI_SSID, WIFI_PASSWORD
from weather import Weather
from buttons import Buttons

class Screen:
    MAIN = 1
    LEFT = 2
    RIGHT = 3
    MOOD_MENU = 4

class TamagotchiApp:
    def __init__(self):
        init_wifi(WIFI_SSID, WIFI_PASSWORD)
        self.display = Display(rotate=90)
        self.display.show()
        self.buttons = Buttons({'left': 20, 'middle': 19, 'right': 18})
        self.current_screen = Screen.MAIN

        self.timer_total_seconds = 120
        self.coffee_timer = CoffeeTimer(total_seconds=self.timer_total_seconds)
        self.coffee_timer_active = False
        self.coffee_anim_frame = 0
        self.last_anim_update = utime.ticks_ms()

        self.mood_menu_active = False
        self.mood_score = 0
        self.display.draw_main_screen()

    def draw_left_screen(self):
        # self.display.clear()
        # self.display.text("LEFT", 0, 0)
        # self.display.text("SCREEN", 0, 10)
        # self.display.text("PLACEHOLDER", 0, 20)
        # self.display.text("TESTTEST", 0, 100)
        # # self.display.draw_cat_from_array(0, 32)
        # self.display.draw_cat(0, 32)
        # self.display.text("TESTTEST", 0, 120)
        self.display.animate_coffee_cup(x=0, y=0, delay_ms=200)

    def open_mood_menu(self):
        self.mood_menu_active = True
        self.display.task_selected_idx = 0
        self.display.draw_mood_menu(mood_score=self.mood_score)

    def screen_navigation_logic(self):
        # LEFT SCREEN LOGIC
        if self.current_screen == Screen.LEFT:
            if self.buttons.was_pressed('right'):
                self.current_screen = Screen.MAIN
                self.display.draw_main_screen(self.mood_score)
            # If left or middle pressed, do nothing (implement later)

        # MIDDLE SCREEN LOGIC
        elif self.current_screen == Screen.MAIN:
            if self.buttons.was_pressed('left'):
                self.current_screen = Screen.LEFT
                self.draw_left_screen()
            elif self.buttons.was_pressed('right'):
                self.current_screen = Screen.RIGHT
                self.display.draw_right_screen(self.coffee_timer)
            elif self.buttons.was_pressed('middle'):
                self.open_mood_menu()

        # RIGHT SCREEN LOGIC
        elif self.current_screen == Screen.RIGHT:
            if self.buttons.was_pressed('left'):
                self.current_screen = Screen.MAIN
                self.display.draw_main_screen(self.mood_score)
            else:
                self.coffee_timer_logic()

    def coffee_timer_logic(self):
        # Handle timer option selection
        if self.buttons.was_pressed('middle'):
            if not self.coffee_timer.running:
                # Start timer
                self.coffee_timer_active = True
                # self.coffee_timer.set_time(2, 0)
                self.coffee_timer.running = True

            else:
                # Stop timer if running
                self.coffee_timer.stop()

        elif self.buttons.was_pressed('right'):
            # Select time for timer
            self.timer_total_seconds += 30
            if self.timer_total_seconds > 180:
                self.timer_total_seconds = 30
            self.coffee_timer.set_time(self.timer_total_seconds)
            self.display.draw_right_screen(self.coffee_timer)
        
        elif self.buttons.was_pressed('left'):
            # Return to main screen
            self.coffee_timer_active = False
            # self.coffee_timer.running = False
            self.current_screen = Screen.MAIN
            self.display.draw_main_screen(self.mood_score)

    def mood_menu_logic(self):
        # Do not now how to implement this yet
        # if len(self.display.task_options) == 1:
        #     self.display.text("Time to", 0, 17, 1)
        #     self.display.text(" Relax", 0, 27, 1)
        #     # self.display.draw_cat(x=0, y=32, key=0)
        #     self.display.show()
        if self.buttons.was_pressed('left'):
            self.display.mood_menu_up()
            self.display.draw_mood_menu(mood_score=self.mood_score)
        elif self.buttons.was_pressed('right'):
            self.display.mood_menu_down()
            self.display.draw_mood_menu(mood_score=self.mood_score)
        elif self.buttons.was_pressed('middle'):
            selected_task = self.display.task_options[self.display.task_selected_idx]
            if selected_task != "EXIT":
                if self.mood_score < self.display.max_mood_score:
                    self.mood_score += 1
                    self.display.task_options.remove(selected_task)
            self.mood_menu_active = False
            self.current_screen = Screen.MAIN
            # return to main screen
            self.display.draw_main_screen(self.mood_score)
    
    def run(self):
        while True:
            self.buttons.update()
            now = utime.ticks_ms()
            if self.mood_menu_active:
                self.mood_menu_logic()
                self.display.show()
            elif self.coffee_timer_active:
                 # Advance animation frame every 200ms if timer is running
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