import urequests
from secrets import WEATHER_API_KEY

class Weather:
    def __init__(self, city):
        self.city = city
        self.url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={WEATHER_API_KEY}&units=metric"

    def get_weather(self):
        # add error handling for network requests
        response = None
        try:
            response = urequests.get(self.url)
            if response.status_code != 200:
                print(f"Bad response: {response.status_code}")
                return None
            data = response.json()
            if data.get("main") and data.get("weather"):
                return {
                    "temp": int(data["main"]["temp"]),
                    "humidity": data["main"]["humidity"],
                    "icon": data["weather"][0]["icon"]
                }
            else:
                print("Incomplete data received")
                return None
        except Exception as e:
            print("Weather fetch error:", e)
            return None
        finally:
            if response:
                response.close()  # Close the response to free up resources