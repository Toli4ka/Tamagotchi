from machine import Pin
import utime
from display import Display
from wifi import init_wifi
from secrets import WIFI_SSID, WIFI_PASSWORD
from weather import Weather
from buttons import Buttons

# Initialize Wi-Fi
init_wifi(WIFI_SSID, WIFI_PASSWORD)

display = Display(rotate=90)
display.show()
# display.animate_ball()
# display.draw_cat(0, 0, width=64, height=64)

# Draw weather data
# weather = Weather("Munich")
# display.draw_weather(weather.get_weather())


BUTTON_PINS = {'left': 20, 'middle': 19, 'right': 18}
buttons = Buttons(BUTTON_PINS)

current_screen = "main"
previous_screen = None

# def draw_screen(screen):
#     # Replace with your actual drawing code
#     print("Drawing:", screen)

# Draw the initial screen
display.draw_main_screen()

while True:
    buttons.update()
    # screen_changed = False

    if buttons.was_pressed('left'):
        if current_screen != "left":
            current_screen = "left"
            display.clear()
            display.draw_smiley_face()
            display.show()
            # screen_changed = True
    elif buttons.was_pressed('right'):
        if current_screen != "right":
            current_screen = "right"
            display.clear()
            display.draw_cat(0, 0, width=64, height=64)
            display.show()
            # screen_changed = True
    elif buttons.was_pressed('middle'):
        if current_screen != "main":
            current_screen = "main"
            # screen_changed = True
            display.draw_main_screen()

    utime.sleep_ms(10)