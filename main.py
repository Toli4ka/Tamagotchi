from machine import Pin
from time import sleep
from display import Display
from wifi import init_wifi
from secrets import WIFI_SSID, WIFI_PASSWORD
from weather import Weather  # Import Weather class

# Initialize Wi-Fi
init_wifi(WIFI_SSID, WIFI_PASSWORD)

display = Display()
display.show()
# display.animate_ball()
# display.draw_cat(0, 0, width=64, height=64)

# Draw weather data
weather = Weather("Munich")
display.draw_weather(weather.get_weather())

