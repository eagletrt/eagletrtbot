import random
from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler


start = ['To', 'Ti', 'Ni', 'No', 'Mi']
end = ['min', 'nin', 'nis', 'mis', 'tis']


def eso(update: Update, _: CallbackContext):
    name = random.choice(start) + random.choice(end)
    surname = random.choice(start) + random.choice(end)
    update.message.reply_text(name + ' ' + surname)


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("eso", eso))