from random import choice

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler

from bot.media import NICO_PATH, PARKING_PATH, TECS_PATHS, ALECS_VOLPE_PATH, BOSE_PATH, PIOVE_PATH


def brao(update: Update, _: CallbackContext):
    with open(choice(TECS_PATHS), "rb") as sticker:
        update.message.reply_sticker(sticker)


def parking(update: Update, _: CallbackContext):
    with open(PARKING_PATH, "rb") as audio:
        update.message.reply_audio(audio)


def bose(update: Update, _: CallbackContext):
    with open(BOSE_PATH, "rb") as audio:
        update.message.reply_audio(audio)


def volpe(update: Update, _: CallbackContext):
    with open(ALECS_VOLPE_PATH, "rb") as audio:
        update.message.reply_audio(audio)


def nico(update: Update, _: CallbackContext):
    with open(NICO_PATH, "rb") as audio:
        update.message.reply_audio(audio)


def piove(update: Update, _: CallbackContext):
    with open(PIOVE_PATH, "rb") as audio:
        update.message.reply_audio(audio)


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
    dispatcher.add_handler(CommandHandler("volpe", volpe))
    dispatcher.add_handler(CommandHandler("nico", nico))
    dispatcher.add_handler(CommandHandler("bose", bose))
    dispatcher.add_handler(CommandHandler("parking", parking))
    dispatcher.add_handler(CommandHandler("piacere", piacere))
    dispatcher.add_handler(CommandHandler("piove", piove))
