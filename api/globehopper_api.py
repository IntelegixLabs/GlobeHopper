import os

import requests
import logging

from flask import Blueprint, jsonify, request
from flask_api import status


from dotenv import load_dotenv

load_dotenv()

WEATHER_RAPID_API_HOST = os.getenv("WEATHER_RAPID_API_HOST")
WEATHER_RAPID_API_KEY = os.getenv("WEATHER_RAPID_API_KEY")

PEXELS_API_HOST = os.getenv("PEXELS_API_HOST")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

globehopper_Blueprint = Blueprint('globehopper_Blueprint', __name__)


@globehopper_Blueprint.route('/demo', methods=['POST'])
def chat_bot():
    try:
        return jsonify({"message": f"Module - Error "}), status.HTTP_400_BAD_REQUEST
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@globehopper_Blueprint.route('/weather', methods=['POST'])
def get_weather_data():
    input_payload = request.get_json(cache=False)
    logging.info("Request to fetch weather Data - %s", input_payload['parameters']['location'])
    location = str(input_payload['parameters']['location'])
    try:
        url = "https://" + WEATHER_RAPID_API_HOST + "/weather"
        querystring = {"location": location, "format": "json", "u": "f"}
        headers = {
            "X-RapidAPI-Key": WEATHER_RAPID_API_KEY,
            "X-RapidAPI-Host": WEATHER_RAPID_API_HOST
        }
        response = requests.get(url, headers=headers, params=querystring)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@globehopper_Blueprint.route('/images', methods=['POST'])
def get_images():
    input_payload = request.get_json(cache=False)
    logging.info("Request to fetch location Data - %s", input_payload['parameters']['location'])
    location = str(input_payload['parameters']['location'])
    query_count = str(input_payload['parameters']['query_count'])
    try:
        url = "https://" + PEXELS_API_HOST + "/v1/search?query=" + location + "&per_page=" + query_count
        headers = {
            "Authorization": PEXELS_API_KEY
        }
        response = requests.get(url, headers=headers)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST
