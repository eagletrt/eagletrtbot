import os
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, PicklePersistence
from bot.commands import brao, fire, odg, punti, simione, spesa, tecsone, tracker

from bot.jobs import scheduler
from bot.conversations import remindme
from bot.tasks import instagram
from bot.database.engine import engine
from bot.database.base import Base
from bot.database.session import Session
from bot.singleton import BOT
from bot.utils import escape, sudo

logger = logging.getLogger(__name__)


def start(update: Update, ctx: CallbackContext) -> None:
    return brao.piacere(update, ctx)


@sudo
def info(update: Update, _: CallbackContext):
    if update.message.reply_to_message is not None:
        user = update.message.reply_to_message.from_user
        chat_id = update.message.reply_to_message.chat_id
        update.message.reply_markdown_v2(
            f"full\_name\=`{escape(user.full_name)}` user\_id\=`{user.id}` chat\_id\=`{chat_id}`"
        )
    else:
        user = update.effective_user
        chat = update.effective_chat
        update.message.reply_markdown_v2(f"user\_id\=`{user.id}` chat\_id\=`{chat.id}`")


def main() -> None:
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

    persistance = PicklePersistence(filename="data/bot.pickle")
    updater = Updater(os.environ["TOKEN"], persistence=persistance)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("info", info))

    remindme.register(dispatcher)
    fire.register(dispatcher)
    brao.register(dispatcher)
    odg.register(dispatcher)
    punti.register(dispatcher)
    simione.register(dispatcher)
    tecsone.register(dispatcher)
    tracker.register(dispatcher)
    spesa.register(dispatcher)

    bot = dispatcher.bot

    BOT.set(bot)

    updater.start_polling()

    instagram_task = scheduler.add_job(
        instagram.task, "interval", minutes=5, jobstore="volatile"
    )

    scheduler.start()

    instagram.task()

    updater.idle()

    instagram_task.remove()
    scheduler.shutdown()


if __name__ == "__main__":
    main()
