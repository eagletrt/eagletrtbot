from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler
import requests
import os

UNSPLASH_ACCESS_KEY=os.environ['UNSPLASH_ACCESS_KEY']


def send_random_monkey_image(update: Update, ctx: CallbackContext):
    api_url = f'https://api.unsplash.com/photos/random?query=monkey&client_id={UNSPLASH_ACCESS_KEY}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        image_url = data['urls']['regular']
        img_data = requests.get(image_url).content
        update.message.bot.send_photo(update.message.chat.id, img_data, reply_to_message_id=update.message.message_id)
    except requests.exceptions.RequestException as e:
        update.message.bot.send_photo(update.message.chat.id,open("bot/media/default_monkey.png","rb"), reply_to_message_id=update.message.message_id)


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("opera", send_random_monkey_image))
