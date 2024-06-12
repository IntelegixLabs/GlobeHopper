import os

import requests
from dotenv import load_dotenv
from requests import Response

load_dotenv()


class APICall:
    """
    This is abstract class for third party api which can use to call third party apis hotels travel etc.
    Inside this class third_party_endpoints function which we can call from outside function without
    initialize APICall class variable.
    """

    def __init__(self, url: str, headers: dict, payload: dict | None = None, query_params: dict | None = None):
        """
        Initialize the url, headers, payload and query_params
        """
        self.__url = url
        self.__headers = headers
        self._payload = payload
        self._query_params = query_params

    def send_request(self) -> Response:
        """
        Here we simply call third party api based on data or query_params
        """
        if self._payload:
            return requests.get(self.__url, data=self._payload, headers=self.__headers)
        elif self._query_params:
            return requests.get(self.__url, params=self._query_params, headers=self.__headers)
        return requests.get(self.__url, headers=self.__headers)

    @staticmethod
    def third_party_endpoints(key: str) -> dict:
        """
        Here we store and map all third party or internal apis in the form of dictionary which
        is takes less storage and memory efficient.
        Here we define third party application data based on application name. example hotels
        However, currently we store hotel api (www.hotels.com).

        :param key: key is the name of third party application which need mapped data need outside to make a request.
        """
        return {
            "hotels": {
                "url": os.environ.get("HOTEL_BASE_URL"),
                "headers": {
                    "X-RapidAPI-Key": os.environ.get("HOTEL_API_KEY"),
                    "X-RapidAPI-Host": os.environ.get("HOTEL_API_HOST")
                }
            },
        }[key]
