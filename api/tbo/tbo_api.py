import os

import requests
import logging
from datetime import datetime, timedelta
import json

from dotenv import load_dotenv
from flask import abort, Blueprint, jsonify, request, Response
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
        return jsonify(response.json()), status.HTTP_200_OK
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
