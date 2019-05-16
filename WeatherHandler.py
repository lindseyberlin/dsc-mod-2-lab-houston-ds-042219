# Importing config.py, which contains the variable API_key
from config import *
# Importing requests library to call API
import requests
#
import json

# Defining a class to contain all functions and attributes related to weather
class WeatherHandler():
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_base_url = f"https://api.darksky.net/forecast/{self.api_key}/"

    def get_weather(self, lat, long, date):
        # Date is coming from our GameDataHandler class
        # Date should be formatted as [yyyy]-[mm]-[dd]
        self.date = date

        self.lat = lat
        self.long = long

        # URL is set based on lat, long, and date
        # Retrieving only daily data, by excluding currently and hourly
        self.url = f"{self.api_base_url}{self.lat},{self.long},{self.date}T20:00:00?exclude=currently, hourly"

        r = requests.get(self.url)

        # 
        is_raining = 0
        if r.status_code == 200:
            raining_target = r.json()["daily"]["data"][0]
            if "precipType" in raining_target.keys():
                if raining_target["precipType"] == "rain":
                    is_raining = 1
        else:
            print("Hit an error.")
        
        return is_raining