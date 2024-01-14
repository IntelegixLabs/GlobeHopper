import os
import re

import cohere
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Chroma

import requests
from dotenv import load_dotenv

load_dotenv()


COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)
PEXELS_API_HOST = os.getenv("PEXELS_API_HOST")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
WEATHER_RAPID_API_HOST = os.getenv("WEATHER_RAPID_API_HOST")
WEATHER_RAPID_API_KEY = os.getenv("WEATHER_RAPID_API_KEY")

embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
db_text_retriever = Chroma(persist_directory="./db/chroma_db_image", embedding_function=embeddings)


def get_pixel_images(location, query_count="2"):
    try:
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


def fetch_hotel_data(location: str):

    try:

        docs = db_text_retriever.similarity_search(location, k=5)

        ans = []
        for i in docs:
            ans.append(i.page_content)

        hotel_data = []

        for item in ans:
            hotel_info = {}
            match_hotel_name = re.search(r'HotelName: ([^\n]+)', item)
            if match_hotel_name:
                hotel_info["HotelName"] = match_hotel_name.group(1)

            match_description = re.findall(r'Description: ([^\n]+)', item)
            if match_description:
                hotel_info["Description"] = match_description

            hotel_rating = re.findall(r'HotelRating: ([^\n]+)', item)
            if hotel_rating:
                hotel_info["HotelRating"] = hotel_rating

            match_images = re.findall(r'Images: ([^\n]+)', item)
            if match_images:
                images_url = str(match_images[0]).split(", ")
                hotel_info["images"] = images_url

            hotel_code = re.findall(r'HotelCode: ([^\n]+)', item)
            if hotel_code:
                hotel_info["HotelCode"] = hotel_code

            address = re.findall(r'Address: ([^\n]+)', item)
            if address:
                hotel_info["Address"] = address

            hotel_facilities = re.findall(r'HotelFacilities: ([^\n]+)', item)
            if hotel_facilities:
                hotel_info["HotelFacilities"] = hotel_facilities

            map_res = re.findall(r'Map: ([^\n]+)', item)
            if map_res:
                hotel_info["Map"] = map_res

            phone_number = re.findall(r'PhoneNumber: ([^\n]+)', item)
            if phone_number:
                hotel_info["PhoneNumber"] = phone_number

            PinCode = re.findall(r'PinCode: ([^\n]+)', item)
            if PinCode:
                hotel_info["PinCode"] = PinCode

            HotelWebsiteUrl = re.findall(r'HotelWebsiteUrl: ([^\n]+)', item)
            if HotelWebsiteUrl:
                hotel_info["HotelWebsiteUrl"] = HotelWebsiteUrl

            hotel_data.append(hotel_info)
        return hotel_data
    except Exception as e:
        print("Error getting location data {}".format(str(e)))
