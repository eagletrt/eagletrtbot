import random
from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler


start = ['To', 'Tho', 'Ti', 'Thi', 'Ni','No', 'Mi']
end = ['min', 'nin', 'ñin', 'nis', 'ñis', 'mis', 'tis', 'mas', 'nas']


def eso(update: Update, _: CallbackContext):
    name = random.choice(start) + random.choice(end)
    surname = random.choice(start) + random.choice(end)
    update.message.reply_text(name + ' ' + surname)


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("eso", eso))
