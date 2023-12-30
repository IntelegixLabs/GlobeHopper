import os

import requests
import logging
from datetime import datetime, timedelta

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
