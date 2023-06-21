import random, requests, datetime
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler


def vsv(update: Update, _: CallbackContext):
    now = datetime.datetime.now().date()
    vsv_date = datetime.date(2023, 7, 6)
    days_to_vsv = (vsv_date - now).days

    html = requests.get('https://www.ladige.it/cultura-e-spettacoli').text
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all('a', class_='article--title')
    titles = [t.text.strip() for t in titles]
    
    premessa = random.choice(['', 'Ragazzi mancano', 'Cittadini, meno', 'Però porca zozza ragazzi mancano'])
    chiusura = random.choice(['', ', fate schifo...', ', non si può andare avanti così.', '... Mi fate venire i brividi.', '... NON VA BENE COSì'])

    txt = "%s %d giorni al VSV e %s%s" % (premessa, days_to_vsv, random.choice(titles), chiusura)
    update.message.reply_text(txt)


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("vsv", vsv))
