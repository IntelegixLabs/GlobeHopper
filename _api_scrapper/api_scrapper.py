import os

import requests
import json
import time
import csv

from dotenv import load_dotenv

load_dotenv()

TBO_URL = os.getenv("TBO_URL")
TBO_KEY = os.getenv("TBO_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + TBO_KEY
}

try:
    get_country_url = TBO_URL + "/TBOHolidays_HotelAPI/CountryList"
    get_country_url_response = requests.get(get_country_url, headers=headers).json()["CountryList"]
    time.sleep(1)

    for county in get_country_url_response:

        CountryCode = county["Code"]
        get_city_list_url = TBO_URL + "/TBOHolidays_HotelAPI/CityList"
        payload_city = json.dumps({
            "CountryCode": CountryCode
        })
        try:
            get_city_list_url_response = requests.post(get_city_list_url, headers=headers, data=payload_city).json()[
                "CityList"]
            time.sleep(1)

            for city in get_city_list_url_response:

                CityCode = city["Code"]
                get_hotel_list_url = TBO_URL + "/TBOHolidays_HotelAPI/TBOHotelCodeList"
                payload_hotel = json.dumps({
                    "CityCode": CityCode,
                    "IsDetailedResponse": "true"
                })
                try:
                    get_hotels_list_url_response = \
                        requests.post(get_hotel_list_url, headers=headers, data=payload_hotel).json()["Hotels"]
                    for hotels in get_hotels_list_url_response:
                        with open('hotels.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(
                                [county["Code"], county["Name"], city["Code"], city["Name"], hotels["HotelCode"],
                                 hotels["HotelName"], hotels["HotelRating"], hotels["Address"],
                                 " ".join(hotels["Attractions"]), hotels["Description"], hotels["FaxNumber"],
                                 " ".join(hotels["HotelFacilities"]), hotels["Map"], hotels["PhoneNumber"],
                                 hotels["PinCode"],
                                 hotels["HotelWebsiteUrl"]])
                        print(county["Code"], county["Name"], city["Code"], city["Name"], hotels["HotelCode"],
                              hotels["HotelName"], hotels["HotelRating"], hotels["Address"],
                              " ".join(hotels["Attractions"]), hotels["Description"], hotels["FaxNumber"],
                              " ".join(hotels["HotelFacilities"]), hotels["Map"], hotels["PhoneNumber"],
                              hotels["PinCode"],
                              hotels["HotelWebsiteUrl"])
                except RuntimeError:
                    continue
        except RuntimeError:
            continue
except RuntimeError as e:
    print(e)
