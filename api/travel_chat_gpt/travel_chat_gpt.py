import logging
import os
import time
import re

import cohere
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request, send_file
from flask_api import status
from langchain.chat_models import ChatCohere
from langchain.embeddings import CohereEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS

load_dotenv()

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)

embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
db_text = Chroma(persist_directory="./db/chroma_db", embedding_function=embeddings)
db_text_retriever = Chroma(persist_directory="./db/chroma_db_image", embedding_function=embeddings)

travel_chat_blp = Blueprint('travel_chat_Blueprint', __name__)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@travel_chat_blp.route('/chat_bot_new', methods=['POST'])
def chat_bot_new():
    inputpayload = request.get_json(cache=False)
    logging.info("Request for chatBot - %s", inputpayload['parameters']['user_message'])
    user_input = str(inputpayload['parameters']['user_message'])
    try:

        chat = ChatCohere()

        retriever = db_text.as_retriever()

        # model = ChatCohere(
        #     streaming=True,
        #     callback_manager=BaseCallbackManager([
        #         StreamingStdOutCallbackHandler()
        #     ]),
        # )

        template = """Fetch hotel names, hotel rating, address, attractions(if any), description, hotel facilities, 
                    map, phone number, pincode, website url below details based only on the following context,
                    if you don't know the answer just say I don't know, don't try to make up:
                    {context}
                    Question: {question}
                    """

        prompt = ChatPromptTemplate.from_template(template)

        chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | chat
                | StrOutputParser()
        )

        response = chain.invoke(user_input)

        docs = db_text_retriever.similarity_search(user_input, k=5)

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
                hotel_info["images"] = match_images

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

        response_bot_message = {"result": response.replace("\n\n", "\n "), "Hotel_Details": hotel_data}

        return jsonify(response_bot_message), status.HTTP_200_OK
    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


def convert_audio_to_text(audio_file):
    r = sr.Recognizer()

    # Load the audio file
    audio = AudioSegment.from_mp3(audio_file)

    # Convert stereo to mono for better recognition
    audio = audio.set_channels(1)

    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)

    # Recognize speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"


@travel_chat_blp.route('/travel_voice_to_text', methods=['POST'])
def travel_voice_to_text():
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400

    audio_file = request.files['file']
    if audio_file.filename == '':
        return {'error': 'No selected file'}, 400

    text_result = "suggest me some hotels in kolkata"

    if audio_file:
        audio_file.save('input.wav')
        time.sleep(10)
        text_result = convert_audio_to_text('input.wav')
        os.remove('input.wav')
        # return jsonify({'text': text_result})

    user_input = text_result
    try:

        chat = ChatCohere()

        retriever = db_text.as_retriever()

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

        tts = gTTS(response, lang='en')
        tts.save('output.mp3')

        return send_file('output.mp3', as_attachment=True), status.HTTP_200_OK

    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST
