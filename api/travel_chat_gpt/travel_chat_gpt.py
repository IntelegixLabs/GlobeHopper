import json
import logging
import os
import time

import cohere
import requests
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request, send_file
from flask_api import status
from langchain.chat_models import ChatCohere
from langchain.embeddings import CohereEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from openai import OpenAI

import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS

load_dotenv()


COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)

embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
db = Chroma(persist_directory="./db/chroma_db", embedding_function=embeddings)

travel_chat_blp = Blueprint('travel_chat_Blueprint', __name__)


@travel_chat_blp.route('/chat_bot', methods=['POST'])
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

        response_bot_message = {"result": response}

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


@travel_chat_blp.route('/travel-voice-to-text', methods=['POST'])
def travel_voice_to_text():
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400

    audio_file = request.files['file']
    if audio_file.filename == '':
        return {'error': 'No selected file'}, 400

    text_result = "suggest me some hotels in kolkata"

    if audio_file:
        audio_file.save('input.mp3')
        time.sleep(10)
        text_result = convert_audio_to_text('input.mp3')
        os.remove('input.mp3')
        # return jsonify({'text': text_result})

    user_input = text_result
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

        tts = gTTS(response, lang='en')
        tts.save('output.mp3')

        return send_file('output.mp3', as_attachment=True), status.HTTP_200_OK

    except Exception as err:
        return jsonify({"message": f"Module - Error - {err}"}), status.HTTP_400_BAD_REQUEST


