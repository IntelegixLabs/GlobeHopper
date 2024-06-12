import os

import requests
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes, Application, \
    ConversationHandler

load_dotenv()

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the token you obtained from BotFather
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Replace 'YOUR_FLASK_API_URL' with the URL of your existing Flask API
FLASK_API_URL = os.getenv('FLASK_API_URL')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Welcome to the GlobeHopper Bot \nSend me a prompt")


# hotel_names = []
# hotels = {}
#
# selected_hotel_name = [None]
# last_photo_position = [0]
class User:
    hotel_names = []
    hotels = {}
    selected_hotel_name = [None]
    last_photo_position = [0]


user_info = {}
keyboard_message = "Select an option from Menu:"


async def handle_message(update: Update, context: CallbackContext):
    print("------------- Few global test --------------")
    user_info[update.message.chat_id] = User()
    print("hotel_names ", user_info[update.message.chat_id].hotel_names)
    print("last_photo_position ", user_info[update.message.chat_id].last_photo_position)
    print("selected_hotel_name ", user_info[update.message.chat_id].selected_hotel_name)

    # update.message.chat_id = User()
    prompt = update.message.text
    prompt_type = update.message.chat.type
    latitude = None
    longitude = None
    if prompt == "Cancel":
        await update.message.reply_text("Thank you for contacting the GlobeHopper Bot",
                                        reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END
    elif prompt in user_info[update.message.chat_id].hotel_names:
        # Generate prompt based on hotel name
        hotel = user_info[update.message.chat_id].hotels.get(prompt)
        user_info[update.message.chat_id].selected_hotel_name[0] = prompt
        await generate_hotel_details(prompt=prompt, hotel=hotel, update=update)
        if latitude and longitude:
            await update.message.reply_location(latitude=latitude, longitude=longitude)
        await get_hotel_photos(update=update, data=hotel)

        keyboard = [['Book hotel 👍', "View more photos"], ["Don't like the hotel?👎 choose different hotel"],
                    ["Cancel"]]
        await update.message.reply_text(
            keyboard_message,
            reply_markup=ReplyKeyboardMarkup(keyboard)
        )
        return ConversationHandler.END
    elif prompt == "Don't like the hotel?👎 choose different hotel":
        user_info[update.message.chat_id].last_photo_position[0] = 0
        keyboard = [
            [user_info[update.message.chat_id].hotel_names[0], user_info[update.message.chat_id].hotel_names[1]],
            [user_info[update.message.chat_id].hotel_names[2], user_info[update.message.chat_id].hotel_names[3]],
            [user_info[update.message.chat_id].hotel_names[4]]]
        await update.message.reply_text(
            keyboard_message,
            reply_markup=ReplyKeyboardMarkup(keyboard)
        )
        return ConversationHandler.END
    elif prompt == "Book hotel 👍":
        # Todo: Will implement booking through telegram
        await update.message.reply_text(
            "Currently you can book hotel from our globehopper website.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    elif prompt == "View more photos":
        # Image handle function
        await get_hotel_photos(update=update, data=user_info[update.message.chat_id].hotels.get(
            user_info[update.message.chat_id].selected_hotel_name[0]))
        keyboard = [['Book hotel 👍', "View more photos"], ["Don't like the hotel?👎 choose different hotel"],
                    ["Cancel"]]
        await update.message.reply_text(
            keyboard_message,
            reply_markup=ReplyKeyboardMarkup(keyboard)
        )
        return ConversationHandler.END

    else:

        try:
            await update.message.reply_text("Please wait while we processing your request 😊")
            response = fetch_response_from_api(prompt)
            await update.message.reply_text(response.get("result"))
        except Exception as e:
            # Handle the "Message is too long" error
            if "Message is too long" in str(e):
                await update.message.reply_text("Sorry, the message is too long to be sent.")
            else:
                # Handle other exceptions
                await update.message.reply_text("An error occurred while processing your request.")
            return ConversationHandler.END

        user_info[update.message.chat_id].hotels.clear()
        user_info[update.message.chat_id].hotel_names.clear()
        user_info[update.message.chat_id].last_photo_position[0] = 0
        for option in response.get("Hotel_Details"):
            user_info[update.message.chat_id].hotels[option.get("HotelName")] = option
            user_info[update.message.chat_id].hotel_names.append(option.get("HotelName"))
        keyboard = [
            [user_info[update.message.chat_id].hotel_names[0], user_info[update.message.chat_id].hotel_names[1]],
            [user_info[update.message.chat_id].hotel_names[2], user_info[update.message.chat_id].hotel_names[3]],
            [user_info[update.message.chat_id].hotel_names[4]]]
        await update.message.reply_text(
            keyboard_message,
            reply_markup=ReplyKeyboardMarkup(keyboard)
        )
        return ConversationHandler.END


async def get_hotel_photos(update, data):
    if data.get("images"):
        try:
            for i in range(user_info[update.message.chat_id].last_photo_position[0],
                           user_info[update.message.chat_id].last_photo_position[0] + 3):
                await update.message.reply_photo(data.get("images")[i])
                user_info[update.message.chat_id].last_photo_position[0] = i + 1
        except IndexError:
            await update.message.reply_text(
                "Sorry for inconvenience, for hotel {} we don't have more photos".format(
                    user_info[update.message.chat_id].selected_hotel_name[0]))
    else:
        await update.message.reply_text(
            "Sorry for inconvenience, for hotel {} we don't have photos".format(
                user_info[update.message.chat_id].selected_hotel_name[0]))


def fetch_response_from_api(prompt: str, url: str = None) -> dict:
    # Make a request to your Flask API
    print("Prompt is: ", prompt)
    payload = {
        "parameters": {
            "user_message": prompt
        }
    }

    if url:
        return requests.post(url, json=payload).json()
    return requests.post(FLASK_API_URL + "/chat_bot_new", json=payload).json()


async def generate_hotel_details(prompt, hotel, update: Update):
    hotel_info = ["Description", "HotelRating", "Address", "HotelFacilities", "Map", "PhoneNumber", "Website"]
    data = {}
    for key in hotel_info:
        if hotel.get(key):
            if key == "Map":
                lat, lon = hotel.get(key)[0].split("|")
                data[key] = f'https://www.google.com/maps?q={lat},{lon}'
            else:
                data[key] = hotel.get(key)[0]
    default_value = "We don't have the information"
    hotel_info = """Here is some information about {}
                Name: {}
                Hotel rating: {}
                Address: {}
                Description: {}
                Hotel facilities: {}
                Map: {}
                Phone number: {}
                Website: {}
                few photos of the hotel below
                Would you like it?
                Choose below options
                """.format(prompt, prompt, data.get("HotelRating", default_value), data.get("Address", default_value),
                           data.get("Description", default_value),
                           data.get("HotelFacilities", default_value), data.get("Map", default_value),
                           data.get("PhoneNumber", default_value),
                           data.get("Website", default_value))

    await update.message.reply_text(hotel_info,
                                    reply_markup=ReplyKeyboardRemove())


async def handle_voice(update: Update, context: CallbackContext) -> None:
    # Handle incoming voice messages
    voice = update.message.voice
    file_id = voice.file_id
    # Download the voice message
    file = await context.bot.get_file(file_id)
    print(file.file_path, file_id)
    # BASE_DIR = Path(__file__).resolve().parent
    # if file.file_path:
    #     file_path = os.path.join(BASE_DIR, "static/telegram-bot/{}-{}".format(update.message.chat.first_name,
    #                                                                           update.message.chat_id))
    #     if not os.path.exists(file_path):
    #         os.makedirs(file_path)
    #     file_path = f"{file_path}/voice{datetime.utcnow()}.ogg"
    audio_file = await file.download_as_bytearray()
    # Prepare the files parameter for the POST request
    files = {'file': ('audio_file.ogg', audio_file, 'audio/ogg')}
    response = requests.post(FLASK_API_URL + "/travel_voice_to_text", files=files)
    await update.message.reply_voice(response.content)


# def send_voice_to_api(voice: str):
#     # Make a request to your Flask API voice search
#     return requests.post(FLASK_API_URL + "/travel_voice_to_text", files=dict(file=voice)).json()


def main() -> None:
    print("starting")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # bot = TelegramBot()
    app.add_handler(CommandHandler(command='start', callback=start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("Polling .... ")
    app.run_polling(poll_interval=5)
    app.idle()


if __name__ == '__main__':
    main()
