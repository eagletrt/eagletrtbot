from telegram import Update
from telegram.ext import (
    CommandHandler, CallbackContext, Dispatcher, CommandHandler    
)
from random import choice
import pyairtable, os, sys, json, time, threading


AIRTABLE_UPDATER_MUTEX = threading.Lock()
LAST_ATTENDANCES_UPDATE = time.time()
MIN_DELTA_REQUESTS = 60
AIRTABLE_TOKEN = os.environ["SECRET_AIRTABLE_TOKEN"]
HR_BASE_ID = os.environ["AIRTABLE_HR_BASE_ID"]
LAB_ATTENDANCES_TABLE_ID=os.environ["AIRTABLE_LAB_ATTENDANCES_TABLE_ID"]
PEOPLE_TABLE_ID=os.environ["AIRTABLE_PEOPLE_TABLE_ID"]
TELEGRAM_TO_EMAIL_CACHE_FP = "telegram_to_email_cache.json"
LAB_ATTENDANCES_CACHE_FD = "lab_attendances_cache.json"


def update_all_caches() -> bool:
    telegram_to_email_cache = {}
    try:
        AIRTABLE_API = pyairtable.Api(AIRTABLE_TOKEN)
        LAB_ATTENDANCES_TABLE = AIRTABLE_API.table(HR_BASE_ID, LAB_ATTENDANCES_TABLE_ID)
        PEOPLE_TABLE = AIRTABLE_API.table(HR_BASE_ID, PEOPLE_TABLE_ID)
    except:
        sys.stdout.write("Error updating caches!")
        return False
    lab_att_cache = LAB_ATTENDANCES_TABLE.all()
    all_people_table = PEOPLE_TABLE.all()
    for record in all_people_table:
        record_data = record["fields"]
        telegram_handle = record_data.get("@Telegram")
        email = record_data.get("Email")
        telegram_to_email_cache[telegram_handle] = email
    with open(LAB_ATTENDANCES_CACHE_FD, "w") as fp:
        json.dump(lab_att_cache, fp)
        fp.close()
    with open(TELEGRAM_TO_EMAIL_CACHE_FP, "w") as fp:
        json.dump(telegram_to_email_cache, fp)
        fp.close()
    return True


def get_lab_attendances_info(username):
    global LAST_ATTENDANCES_UPDATE
    telegram_to_email_file = open(TELEGRAM_TO_EMAIL_CACHE_FP)
    TELEGRAM_TO_EMAIL = json.load(telegram_to_email_file)
    lab_attendances_cache_file = open(LAB_ATTENDANCES_CACHE_FD)
    LAB_ATTENDANCES_CACHE = json.load(lab_attendances_cache_file)
    telegram_to_email_file.close()
    lab_attendances_cache_file.close()
    current_time = time.time()
    if (current_time - LAST_ATTENDANCES_UPDATE) > MIN_DELTA_REQUESTS:
        LAST_ATTENDANCES_UPDATE = current_time
        if not update_all_caches():
            return "Mmm, non riesco a scaricare nuovi dati... riprova più tardi..."
    username_with_handle = "@" + username
    email = TELEGRAM_TO_EMAIL.get(username)
    email_with_handle = TELEGRAM_TO_EMAIL.get(username_with_handle)
    if email == None and email_with_handle == None:
        return "Oh no cara, mi risulta che tu non esista. Contatta qualcuno.\n"
    if email == None:
        email = email_with_handle
    for record in LAB_ATTENDANCES_CACHE:
        data = record["fields"]
        cemail = data.get("email")
        if email == cemail:
            ore_mese_corrente = data["Ore mese corrente"]
            return "Mi risulta che finora tu {} abbia trascorso {} ore nel laboratorio di E-Agle TRT questo mese".format(
                username_with_handle,
                str(round(ore_mese_corrente, 2))
            )
    return "Oh no, sembra che tu non sia mai stato in lab."


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
