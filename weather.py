from time import sleep
import urequests
from secrets import WEATHER_API_KEY

class Weather:
    def __init__(self, city):
        self.city = city
        self.url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={WEATHER_API_KEY}&units=metric"
        
    def get_weather(self):
        response = urequests.get(self.url)
        data = response.json()
        response.close()  # Close the response to free up resources
        if data.get("main") and data.get("weather"):
            temp = data["main"]["temp"]
            desc = data["weather"][0]["main"]
            humidity = data["main"]["humidity"]
            if desc == "Clouds":
                desc = "Cloudy"
            elif desc == "Clear":
                desc = "Sunny"
            elif desc == "Rain":
                desc = "Rainy"
            elif desc == "Snow":
                desc = "Snowy"
            else:
                desc = "Weather not recognized"
            return f"{self.city}\nTemp: {int(temp)}C\n{desc}\nHum: {humidity}%"
        else:
            return "No data"
