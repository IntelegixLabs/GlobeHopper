from flask import abort, Response

from utils.api_utils import APICall


class Hotels:
    """
    This is class of hotel, in which we have hotels data which comes from www.hotels.com api.

    """

    def __init__(self, path: str, payload: dict | None = None):
        """
        Initialize the path or slug of the endpoint.
        Initialize the payload or body data
        """
        self.api_call = None
        self.endpoints = None
        self.payload = payload
        self.path = path

    def build_request(self, query_params: dict | None = None) -> Response:
        """
        To build the full-fledged request, first need to get callable url and headers from APICall,
        then if callable endpoint (www.hotels.com) is found we build the endpoint and make a request.
        if callable endpoint not found we simply return error with unprocessable entry code.
        """
        self.endpoints = APICall.third_party_endpoints("hotels")
        if self.endpoints["url"] is None:
            return abort(422, "Callable endpoint is not found")
        self.api_call = APICall(self.endpoints["url"] + self.path, self.endpoints["headers"], self.payload,
                                query_params=query_params)
        return self.api_call.send_request()


def get_city_id(query_location: str, country: str, locale: str) -> dict:
    """
    Get city id or region id from hotels api.
    :param query_location: this is actual city or location or area name
    :param country: this is country code. example for India would be IN
    :param locale: This is localization. example for India would be en_IN
    """
    hotel_api = Hotels("/v2/regions")
    querystring = {"query": query_location, "domain": country, "locale": locale}
    res = hotel_api.build_request(query_params=querystring)
    return {"city_id": res.json()["cityId"]}
