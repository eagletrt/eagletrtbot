from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler
import requests
import os

UNSPLASH_ACCESS_KEY=os.environ['UNSPLASH_ACCESS_KEY']

def send_photo(update: Update, query: str, default_path: str):
    api_url = f'https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        image_url = data['urls']['regular']
        img_data = requests.get(image_url).content
        update.message.bot.send_photo(update.message.chat.id, img_data, reply_to_message_id=update.message.message_id)
    except requests.exceptions.RequestException as e:
        update.message.bot.send_photo(update.message.chat.id,open(default_path,"rb"), reply_to_message_id=update.message.message_id)  


def send_random_monkey_image(update: Update, ctx: CallbackContext):
    send_photo(update, "monkey", "bot/media/default_monkey.png")

def send_random_paste_image(update: Update, ctx: CallbackContext):
    send_photo(update, "pastries", "bot/media/default_pastries.png")

def send_random_transparent_stuff_image(update: Update, ctx: CallbackContext):
    send_photo(update, "work gloves", "bot/media/default_transparent.jpg")


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("opera", send_random_monkey_image))
    dispatcher.add_handler(CommandHandler("simia", send_random_monkey_image))
    dispatcher.add_handler(CommandHandler("paste", send_random_paste_image))
    dispatcher.add_handler(CommandHandler("fastenal", send_random_transparent_stuff_image))
