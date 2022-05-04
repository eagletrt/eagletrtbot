from random import choice

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler

from bot.media import PARKING_SHORT_PATH, TECS_PATHS
from bot.utils import only_eagle


@only_eagle
def brao(update: Update, _: CallbackContext):
    with open(choice(TECS_PATHS), "rb") as sticker:
        update.message.reply_sticker(sticker)


@only_eagle
def parking(update: Update, _: CallbackContext):
    with open(PARKING_SHORT_PATH, "rb") as audio:
        update.message.reply_audio(audio)


@only_eagle
def piacere(update: Update, _: CallbackContext):
    update.message.reply_markdown_v2(
        """Piacere cara, sono *T\.E\.C\.S\.*
👷‍♂️ *T*ecnico
⚡ *E*lettronico
👨‍💼 *C*apo
🍆 *S*exy
"""
    )


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("brao", brao))
    dispatcher.add_handler(CommandHandler("parking", parking))
    dispatcher.add_handler(CommandHandler("piacere", piacere))
