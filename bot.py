import os
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, PicklePersistence, MessageHandler, Filters
from bot.commands import brao, random_photo, tonis, fire, odg, punti, simione, spesa, tecsone, tracker, vsv, ore_lab, custom_tags

from bot.jobs import scheduler
from bot.conversations import remindme
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
    custom_tags.add_custom_tag(dispatcher, '@ct', custom_tags.custom_tag_ct)
    custom_tags.add_custom_tag(dispatcher, '@drivers', custom_tags.custom_tag_drivers)
    custom_tags.add_custom_tag(dispatcher, '@driver', custom_tags.custom_tag_drivers)
    custom_tags.add_custom_tag(dispatcher, '@pm', custom_tags.custom_tag_pm)
    custom_tags.add_custom_tag(dispatcher, '@hr', custom_tags.custom_tag_pm)
    custom_tags.add_custom_tag(dispatcher, '@sw', custom_tags.custom_tag_sw)
    custom_tags.add_custom_tag(dispatcher, '@hw', custom_tags.custom_tag_hw)
    custom_tags.add_custom_tag(dispatcher, '@dmt', custom_tags.custom_tag_dmt)
    custom_tags.add_custom_tag(dispatcher, '@mt', custom_tags.custom_tag_mt)
    custom_tags.add_custom_tag(dispatcher, '@cm', custom_tags.custom_tag_cm)
    custom_tags.add_custom_tag(dispatcher, '@mgt', custom_tags.custom_tag_mgt)
    custom_tags.add_custom_tag(dispatcher, '@inlab', custom_tags.custom_tag_in_lab)
    
    custom_tags.add_custom_tag(dispatcher, '@telemetry', custom_tags.custom_tag_wg_telemetry)
    custom_tags.add_custom_tag(dispatcher, '@micro', custom_tags.custom_tag_wg_micro)
    custom_tags.add_custom_tag(dispatcher, '@compositi', custom_tags.custom_tag_wg_composites)
    custom_tags.add_custom_tag(dispatcher, '@powertrain', custom_tags.custom_tag_wg_powertrain)

    remindme.register(dispatcher)
    fire.register(dispatcher)
    brao.register(dispatcher)
    tonis.register(dispatcher)
    odg.register(dispatcher)
    punti.register(dispatcher)
    simione.register(dispatcher)
    tecsone.register(dispatcher)
    tracker.register(dispatcher)
    spesa.register(dispatcher)
    vsv.register(dispatcher)
    ore_lab.register(dispatcher)
    random_photo.register(dispatcher)
    custom_tags.register(dispatcher)

    bot = dispatcher.bot

    BOT.set(bot)

    updater.start_polling()

    scheduler.start()

    updater.idle()

    scheduler.shutdown()


if __name__ == "__main__":
    main()
