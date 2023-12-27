import os

import requests
import logging
import json

from flask import Blueprint, jsonify, request
from flask_api import status
import cohere

from langchain.chat_models import ChatCohere
from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv

load_dotenv()

WEATHER_RAPID_API_HOST = os.getenv("WEATHER_RAPID_API_HOST")
WEATHER_RAPID_API_KEY = os.getenv("WEATHER_RAPID_API_KEY")

PEXELS_API_HOST = os.getenv("PEXELS_API_HOST")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)

embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
db = Chroma(persist_directory="./db/chroma_db", embedding_function=embeddings)

globehopper_Blueprint = Blueprint('globehopper_Blueprint', __name__)


@globehopper_Blueprint.route('/demo', methods=['POST'])
def chat_botx():
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
    destination = str(input_payload['parameters']['destination'])

    try:
        source = str(input_payload['parameters']['source'])
        start_date = str(input_payload['parameters']['start_date'])
        end_date = str(input_payload['parameters']['end_date'])
    except:
        source = "Kolkata"
        start_date = "2023-12-10"
        end_date = "2023-12-15"

    # start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
    # end_date = date(int(end_date[2]), int(end_date[1]), int(end_date[0]))
    try:
        prompt = """Consider yourself a travel planner. Show me day wise planner for all days from """ + str(
            start_date) + """ to """ + str(end_date) + """Display the output in form of valid JSON object:
                { "introduction": "Give brief description about """ + str(destination) + """ ",
                 "itinerary": 
                    [
                        { 
                            "Day": "Day number follow format as 1" ,
                            "morning": "suggest popular restaurants to have breakfast, suggest places of interest, commute to places" ,
                            "afternoon": "suggest popular restaurants to have lunch, suggest places of interest, commute to places"  ,
                            "evening": "suggest popular restaurants to have snacks and party, suggest places of interest, commute to places" ,
                            "night": "suggest popular restaurants to have dinner, suggest places of interest, commute to places"
                        }
                    ] 
                }"""

        response = co.generate(
            model='command-nightly',
            prompt=prompt,
            # temperature=5,
            # max_tokens=2048,
        )

        res = response.generations[0].text

        # Replace "\n\n" with actual newline characters
        formatted_text = res.replace("\\n\\n", "\n")

        start_index, end_index = 0, -1

        for i in range(0, len(formatted_text)):
            if formatted_text[i:i + 7] == "```json":
                start_index = i + 7
                break

        for i in range(len(formatted_text), -1, -1):
            if formatted_text[i:i + 3] == "```":
                end_index += i
                break

        formatted_text = formatted_text[start_index:end_index]

        try:
            logging.info("Prompt generated to fetch travel_plan - %s", formatted_text)
            formatted_text = json.loads(formatted_text)
        except:
            pass

        return jsonify(formatted_text), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@globehopper_Blueprint.route('/list_famous_destinations', methods=['POST'])
def list_famous_destinations():
    input_payload = request.get_json(cache=False)
    logging.info("Request for List of Famous Destinations - %s", input_payload['parameters'])

    try:
        travel_destination = str(input_payload['parameters']['travel_destination'])
    except:
        travel_destination = "Europe"

    try:
        prompt = """Consider yourself a travel planner. List of famous travel Destinations city in """ + str(
            travel_destination) + """,Display the output in form of valid JSON object:
                { "city": "List of city names" }
                """

        response = co.generate(
            model='command-nightly',
            prompt=prompt,
            # temperature=5,
            # max_tokens=2048,
        )

        res = response.generations[0].text

        # Replace "\n\n" with actual newline characters
        formatted_text = res.replace("\\n\\n", "\n")

        start_index, end_index = 0, -1

        for i in range(0, len(formatted_text)):
            if formatted_text[i:i + 7] == "```json":
                start_index = i + 7
                break

        for i in range(len(formatted_text), -1, -1):
            if formatted_text[i:i + 3] == "```":
                end_index += i
                break

        formatted_text = formatted_text[start_index:end_index]

        try:
            logging.info("Prompt generated List of Famous Destinations - %s", formatted_text)
            formatted_text = json.loads(formatted_text)
        except:
            pass

        return jsonify(formatted_text), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


@globehopper_Blueprint.route('/chat_bot', methods=['POST'])
def chat_bot():
    inputpayload = request.get_json(cache=False)
    logging.info("Request for chatBot - %s", inputpayload['parameters']['user_message'])
    user_input = str(inputpayload['parameters']['user_message'])
    try:

        chat = ChatCohere()

        retriever = db.as_retriever()

        template = """Fetch hotel names, hotel rating, address, attractions(if any), description, hotel facilities, 
        map, phone number, pincode, website url below details based only on the following context,
        if you don't know the answer just say I don't know, don't try to make up:
        {context}
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | chat
                | StrOutputParser()
        )

        response = chain.invoke(user_input)

        return jsonify(response), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST
