from time import sleep
import urequests
from secrets import WEATHER_API_KEY

class Weather:
    def __init__(self, city):
        self.city = city
        self.url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={WEATHER_API_KEY}&units=metric"
        
    def get_weather(self):
        # add error handling for network requests
        try:
            response = urequests.get(self.url)
            if response.status_code != 200:
                raise Exception(f"Bad response: {response.status_code}")
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
        data = response.json()
        response.close()  # Close the response to free up resources
        if data.get("main") and data.get("weather"):
            temp = data["main"]["temp"]
            desc = data["weather"][0]["main"]
            humidity = data["main"]["humidity"]
            return {"temp": int(temp), "humidity": humidity, "desc": desc}
        else:
            return None
