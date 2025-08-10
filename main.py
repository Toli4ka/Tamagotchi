from machine import Pin
import utime
from display import Display
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
        self.mood_menu_active = False
        self.mood_score = 0
        self.display.draw_main_screen()

    def draw_left_screen(self):
        self.display.clear()
        self.display.text("LEFT", 0, 0)
        self.display.text("SCREEN", 0, 10)
        self.display.text("PLACEHOLDER", 0, 20)
        self.display.text("TESTTEST", 0, 100)
        self.display.draw_cat_from_array(0, 32)
        self.display.text("TESTTEST", 0, 120)

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
                self.display.draw_right_screen()
            elif self.buttons.was_pressed('middle'):
                self.open_mood_menu()

        # RIGHT SCREEN LOGIC
        elif self.current_screen == Screen.RIGHT:
            if self.buttons.was_pressed('left'):
                self.current_screen = Screen.MAIN
                self.display.draw_main_screen(self.mood_score)
            elif self.buttons.was_pressed('middle'):
                # Implement option selection logic here (SET, START, STOP)
                pass
            elif self.buttons.was_pressed('right'):
                # Implement marker movement logic here
                pass

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
            if self.mood_menu_active:
                self.mood_menu_logic()
                self.display.show()
            else:
                self.screen_navigation_logic()
                self.display.show()
            utime.sleep_ms(10)

if __name__ == "__main__":
    app = TamagotchiApp()
    app.run()