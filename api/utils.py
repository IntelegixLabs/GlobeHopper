import os

import requests
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_HOST = os.getenv("PEXELS_API_HOST")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
WEATHER_RAPID_API_HOST = os.getenv("WEATHER_RAPID_API_HOST")
WEATHER_RAPID_API_KEY = os.getenv("WEATHER_RAPID_API_KEY")


def get_pixel_images(location, query_count="2",orientation=None):
    try:
        if orientation:
            url = "https://" + PEXELS_API_HOST + "/v1/search?query=" + location + "&per_page=" + query_count + "&orientation=" + orientation
        else:
            url = "https://" + PEXELS_API_HOST + "/v1/search?query=" + location + "&per_page=" + query_count
        headers = {
            "Authorization": PEXELS_API_KEY
        }
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print("Error getting pixel images: " + str(e))


def fetch_weather_data(location: str):
    try:
        url = "https://" + WEATHER_RAPID_API_HOST + "/weather"
        querystring = {"location": location, "format": "json", "u": "f"}
        headers = {
            "X-RapidAPI-Key": WEATHER_RAPID_API_KEY,
            "X-RapidAPI-Host": WEATHER_RAPID_API_HOST
        }
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()
    except Exception as e:
        print("Error getting weather data {}".format(str(e)))
