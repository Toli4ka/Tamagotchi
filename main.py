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
mood_menu_active = False

# Draw the initial screen
display.draw_main_screen()

while True:
    buttons.update()
    
    if mood_menu_active:
        # Mood menu navigation
        if buttons.was_pressed('left'):
            display.mood_menu_up()
            display.draw_cat(x=0, y=32, key=0)
            # display.draw_main_screen(cat_x=0, cat_y=0)
            display.draw_mood_menu()
        elif buttons.was_pressed('right'):
            display.mood_menu_down()
            display.draw_cat(x=0, y=32, key=0)
            # display.draw_main_screen(cat_x=0, cat_y=0)
            display.draw_mood_menu()
        elif buttons.was_pressed('middle'):
            # If EXIT is selected, close menu and return to main screen
            if display.mood_options[display.mood_selected_idx] == "EXIT":
                mood_menu_active = False
                current_screen = "main"
                display.draw_main_screen()
            else:
                # Handle selection (add your logic here)
                print(f"Selected mood: {display.mood_options[display.mood_selected_idx]}")
                # display.text(f"Selected: {display.mood_options[display.mood_selected_idx]}", 0, 50)
        display.show()
    else:
        # Screen navigation logic
        if buttons.was_pressed('left'):
            if current_screen != "left":
                current_screen = "left"
                display.clear()
                display.text("TESTTEST", 0, 100)
                display.draw_cat(0, 64)
                display.text("TESTTEST", 0, 120)
                # display.show()
                # screen_changed = True
        elif buttons.was_pressed('right'):
            if current_screen != "right":
                current_screen = "right"
                display.clear()
                display.text("TESTTEST", 0, 10)
                display.draw_mood_menu()
                # display.show()
                # screen_changed = True
        elif buttons.was_pressed('middle'):
            if current_screen != "main":
                current_screen = "main"
                # screen_changed = True
                display.draw_main_screen()
            else:
                # Need to redraw, otherwise the screen is not updated correctly
                # display.draw_main_screen(cat_x=0, cat_y=0)
                display.draw_cat(x=0, y=32, key=0)
                # Open mood menu
                mood_menu_active = True
                display.mood_selected_idx = 0  # Reset selection
                display.draw_mood_menu()
    display.show()

    utime.sleep_ms(10)