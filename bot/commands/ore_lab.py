from telegram import Update
from telegram.ext import (
    CommandHandler, CallbackContext, Dispatcher, CommandHandler    
)
from random import choice
import sys, json
from bot.commands.utils.airtable_utils import *


def get_lab_attendances_info(username):
    if not airtable_caches_updater():
        return "Mmm, non riesco a scaricare nuovi dati... riprova più tardi..."
    
    telegram_to_email_file = open(TELEGRAM_TO_EMAIL_CACHE_FP)
    telegram_to_email = json.load(telegram_to_email_file)
    lab_attendances_cache_file = open(LAB_ATTENDANCES_CACHE_FD)
    lab_attendances_cache = json.load(lab_attendances_cache_file)
    telegram_to_email_file.close()
    lab_attendances_cache_file.close()
    
    username_with_handle = "@" + username
    email = telegram_to_email.get(username) or telegram_to_email.get(username_with_handle)
    if email == None:
        return "Oh no cara, mi risulta che tu non esista. Contatta qualcuno.\n"
    for record in lab_attendances_cache:
        data = record["fields"]
        cemail = data.get("email")
        if email == cemail:
            ore_mese_corrente = data["Ore mese corrente"]
            return "Mi risulta che finora tu {} abbia trascorso {} ore nel laboratorio di E-Agle TRT questo mese".format(
                username_with_handle,
                str(round(ore_mese_corrente, 2))
            )
    return "Oh no, sembra che tu non sia mai stato in lab."


def get_lab_presence(username) -> bool:
    if not airtable_caches_updater():
        return "Mmm, non riesco a scaricare nuovi dati... riprova più tardi..."
    
    telegram_to_email_file = open(TELEGRAM_TO_EMAIL_CACHE_FP)
    telegram_to_email = json.load(telegram_to_email_file)
    lab_attendances_cache_file = open(LAB_ATTENDANCES_CACHE_FD)
    lab_attendances_cache = json.load(lab_attendances_cache_file)
    telegram_to_email_file.close()
    lab_attendances_cache_file.close()

    username_with_handle = "@" + username
    email = telegram_to_email.get(username) or telegram_to_email.get(username_with_handle)
    if email == None:
        return "Oh no cara, mi risulta che tu non esista. Contatta qualcuno.\n"
    for record in lab_attendances_cache:
        data = record["fields"]
        cemail = data.get("email")
        if email == cemail:
            try:
                presente_in_lab = data.get("Presente in Lab")
                if presente_in_lab:
                    return "Risulti attualmente presente in lab"
                else:
                    return "Attualmente non risulti presente in lab"
            except:
                return "Errore Tecnico, riprova tra un attimo"
    return "Oh no, sembra che tu non sia mai stato in lab."


def presente_in_lab(update: Update, ctx: CallbackContext) -> None:
    username = update.message.from_user.username
    if AIRTABLE_UPDATER_MUTEX.locked():
        return update.message.reply_text(
            f"Mi dispiace. Sono impegnata al momento. Riprova giusto tra un paio di secondi."
        )
    AIRTABLE_UPDATER_MUTEX.acquire()
    message = get_lab_presence(username)
    AIRTABLE_UPDATER_MUTEX.release()
    return update.message.reply_text(f"{message}")
    

def ore(update: Update, ctx: CallbackContext) -> None:
    username = update.message.from_user.username
    # username = update.message.chat.username
    # chat_id = update.message.chat_id # TODO save the chat id somewhere, so we can contact the person directly if needed.
    if AIRTABLE_UPDATER_MUTEX.locked():
        return update.message.reply_text(
            f"Mi dispiace. Sono impegnata al momento. Riprova giusto tra un paio di secondi."
        )
    AIRTABLE_UPDATER_MUTEX.acquire()
    message = get_lab_attendances_info(username)
    AIRTABLE_UPDATER_MUTEX.release()
    return update.message.reply_text(f"{message}")


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    if not update_all_caches():
        sys.stderr.write(
            "[FATAL ERROR]: Could not connect to airtable api's at start. Exiting..."
        )
        exit(1)
    dispatcher.add_handler(CommandHandler("ore", ore))
    dispatcher.add_handler(CommandHandler("inlab", presente_in_lab))

