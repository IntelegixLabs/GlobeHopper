import os

import requests
import logging
import json

from flask import Blueprint, jsonify, request
from flask_api import status
import cohere

from datetime import date
from dotenv import load_dotenv

load_dotenv()

WEATHER_RAPID_API_HOST = os.getenv("WEATHER_RAPID_API_HOST")
WEATHER_RAPID_API_KEY = os.getenv("WEATHER_RAPID_API_KEY")

PEXELS_API_HOST = os.getenv("PEXELS_API_HOST")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)

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


@globehopper_Blueprint.route('/video', methods=['POST'])
def get_videos():
    input_payload = request.get_json(cache=False)
    logging.info("Request to fetch location Data - %s", input_payload['parameters']['location'])
    location = str(input_payload['parameters']['location'])
    query_count = str(input_payload['parameters']['query_count'])
    try:
        url = "https://" + PEXELS_API_HOST + "/videos/search?query=" + location + "&per_page=" + query_count
        headers = {
            "Authorization": PEXELS_API_KEY
        }
        response = requests.get(url, headers=headers)
        return jsonify(response.json()), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@globehopper_Blueprint.route('/travel_planner', methods=['POST'])
def travel_planner():
    input_payload = request.get_json(cache=False)
    logging.info("Request for travel_plan - %s", input_payload['parameters'])
    source = str(input_payload['parameters']['source'])
    destination = str(input_payload['parameters']['destination'])
    start_date = str(input_payload['parameters']['start_date']).split("-")
    end_date = str(input_payload['parameters']['end_date']).split("-")
    start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
    end_date = date(int(end_date[2]), int(end_date[1]), int(end_date[0]))
    try:
        prompt = ("Context - Consider yourself a travel planner. Show me day wise planner for all days from " + str(
            start_date) + " to " + str(end_date) + "Display the output in form of JSON object:\
            {trip-planner:[{intro : about_" + destination + ".},{flights: suggest flights to take from "
            + source + " to " + destination + "},{ hotel: suggest popular hotel_names}, {dates:" + str(start_date) +
            " to " + str(end_date) + ".},{itinerary: from " + str(start_date) + " to " + str(end_date) + ". [Day: number,[\
            { morning: suggest popular restaurants to have breakfast, suggest places of interest, commute to places},\
            {afternoon: suggest popular restaurants to have lunch, suggest places of interest, commute to places},\
            {evening: suggest popular restaurants to have dinner, suggest places of interest, commute to places},\
            ],{return: suggest return flights to take},],}, ], }")

        logging.info("Prompt generated to fetch travel_plan - %s", prompt)

        response = co.generate(
            model='command-nightly',
            prompt=prompt,
            # temperature=5,
            # max_tokens=2048,
        )

        res = response.generations[0].text

        # Replace "\n\n" with actual newline characters
        formatted_text = res.replace("\\n\\n", "\n")
        formatted_text = json.dumps(formatted_text)

        print(formatted_text)

        return jsonify(formatted_text), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST
