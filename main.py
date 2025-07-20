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
        self.display.draw_main_screen()

    def draw_left_screen(self):
        self.display.clear()
        self.display.text("LEFT", 0, 20)
        self.display.text("SCREEN", 0, 30)
        self.display.text("PLACEHOLDER", 0, 40)
        self.display.text("TESTTEST", 0, 100)
        self.display.draw_cat(0, 64)
        self.display.text("TESTTEST", 0, 120)

    def draw_right_screen(self):
        self.display.clear()
        self.display.text("TESTTEST", 0, 10)
        self.display.text("RIGHT", 0, 20)
        self.display.text("SCREEN", 0, 30)
        self.display.text("PLACEHOLDER", 0, 40)
        # self.display.draw_mood_menu()

    def draw_main_screen(self):
        self.display.draw_main_screen()

    def open_mood_menu(self):
        self.display.draw_cat(x=0, y=32, key=0)
        self.mood_menu_active = True
        self.display.mood_selected_idx = 0
        self.display.draw_mood_menu()

    def screen_navigation_logic(self):
        if self.buttons.was_pressed('left') and self.current_screen != Screen.LEFT:
            self.current_screen = Screen.LEFT
            self.draw_left_screen()
        elif self.buttons.was_pressed('right') and self.current_screen != Screen.RIGHT:
            self.current_screen = Screen.RIGHT
            self.draw_right_screen()
        elif self.buttons.was_pressed('middle'):
            if self.current_screen != Screen.MAIN:
                self.current_screen = Screen.MAIN
                self.draw_main_screen()
            else:
                self.open_mood_menu()

    def mood_menu_logic(self):
        if self.buttons.was_pressed('left'):
            self.display.mood_menu_up()
            self.display.draw_cat(x=0, y=32, key=0)
            self.display.draw_mood_menu()
        elif self.buttons.was_pressed('right'):
            self.display.mood_menu_down()
            self.display.draw_cat(x=0, y=32, key=0)
            self.display.draw_mood_menu()
        elif self.buttons.was_pressed('middle'):
            if self.display.mood_options[self.display.mood_selected_idx] == "EXIT":
                self.mood_menu_active = False
                self.current_screen = Screen.MAIN
                self.draw_main_screen()
            else:
                print(f"Selected mood: {self.display.mood_options[self.display.mood_selected_idx]}")

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