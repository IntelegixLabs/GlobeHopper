import os

import requests
import json

from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from flask_api import status

load_dotenv()


TBO_URL = os.getenv("TBO_URL")
TBO_KEY = os.getenv("TBO_KEY")

tbo_blp = Blueprint('tbo_Blueprint', __name__)


@tbo_blp.route('/TBOHolidays_HotelAPI/CountryList', methods=['GET'])
def get_country_list():
    try:
        url = TBO_URL + "/TBOHolidays_HotelAPI/CountryList"
        payload = {}
        headers = {
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/HotelSearch', methods=['POST'])
def hotel_search():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/HotelSearch"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/HotelCancellationPolicyForAllRooms', methods=['POST'])
def hotel_cancellation_policy_all_rooms():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/HotelCancellationPolicyForAllRooms"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/AvailableHotelRooms', methods=['POST'])
def available_hotel_rooms():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/AvailableHotelRooms"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/HotelCancellationPolicy', methods=['POST'])
def hotel_cancellation_policy():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/HotelCancellationPolicy"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/Prebook', methods=['POST'])
def pre_book():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/Prebook"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/HotelBook', methods=['POST'])
def hotel_book():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/HotelBook"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/BookingDetail', methods=['POST'])
def booking_detail():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/BookingDetail"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/Cancel', methods=['POST'])
def cancel():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/Cancel"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/Hoteldetails', methods=['POST'])
def hotel_details():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/Hoteldetails"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        response = response.json()

        response_output = {}

        try:
            Address = response["HotelDetails"][0]["Address"]
        except:
            Address = None

        try:
            Attractions = response["HotelDetails"][0]["Attractions"]
        except:
            Attractions = None

        try:
            CheckInTime = response["HotelDetails"][0]["CheckInTime"]
        except:
            CheckInTime = None

        try:
            CheckOutTime = response["HotelDetails"][0]["CheckOutTime"]
        except:
            CheckOutTime = None

        try:
            CityId = response["HotelDetails"][0]["CityId"]
        except:
            CityId = None

        try:
            CityName = response["HotelDetails"][0]["CityName"]
        except:
            CityName = None

        try:
            CountryCode = response["HotelDetails"][0]["CountryCode"]
        except:
            CountryCode = None

        try:
            CountryName = response["HotelDetails"][0]["CountryName"]
        except:
            CountryName = None

        try:
            Description = response["HotelDetails"][0]["Description"]
        except:
            Description = None

        try:
            FaxNumber = response["HotelDetails"][0]["FaxNumber"]
        except:
            FaxNumber = None

        try:
            HotelCode = response["HotelDetails"][0]["HotelCode"]
        except:
            HotelCode = None

        try:
            HotelFacilities = response["HotelDetails"][0]["HotelFacilities"]
        except:
            HotelFacilities = None

        try:
            HotelName = response["HotelDetails"][0]["HotelName"]
        except:
            HotelName = None

        try:
            HotelRating = response["HotelDetails"][0]["HotelRating"]
        except:
            HotelRating = None

        try:
            Images = response["HotelDetails"][0]["Images"]
        except:
            Images = None

        try:
            Map = response["HotelDetails"][0]["Map"]
        except:
            Map = None

        try:
            PhoneNumber = response["HotelDetails"][0]["PhoneNumber"]
        except:
            PhoneNumber = None

        try:
            PinCode = response["HotelDetails"][0]["PinCode"]
        except:
            PinCode = None

        response_output["data"] = [{"Address": Address, "Attractions": Attractions, "CheckInTime": CheckInTime,
                                    "CheckOutTime": CheckOutTime, "CityId": CityId, "CityName": CityName,
                                    "CountryCode": CountryCode, "CountryName": CountryName, "Description": Description,
                                    "FaxNumber": FaxNumber, "HotelCode": HotelCode, "HotelFacilities": HotelFacilities,
                                    "HotelName": HotelName, "HotelRating": HotelRating, "Images": Images, "Map": Map,
                                    "PhoneNumber": PhoneNumber, "PinCode": PinCode}]

        return jsonify(response_output), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/BookingDetailsBasedOnDate', methods=['POST'])
def booking_details_based_on_date():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/BookingDetailsBasedOnDate"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/CityList', methods=['POST'])
def city_list():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/CityList"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/TBOHotelCodeList', methods=['POST'])
def hotel_code_list():
    try:
        input_payload = request.get_json(cache=False)
        url = TBO_URL + "/TBOHolidays_HotelAPI/TBOHotelCodeList"
        payload = json.dumps(input_payload)
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@tbo_blp.route('/TBOHolidays_HotelAPI/hotelcodelist', methods=['GET'])
def get_hotel_code_list():
    try:
        url = TBO_URL + "/TBOHolidays_HotelAPI/hotelcodelist"
        payload = {}
        headers = {
            "Authorization": "Basic " + TBO_KEY
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST
