from datetime import datetime
import logging

import dateparser

from telegram import ForceReply, Update
from telegram.ext import (
    Dispatcher,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from sqlalchemy import Column, Integer, Sequence, String, DateTime, func

from bot.database.base import Base
from bot.database.session import Session
from bot.jobs import scheduler
from bot.singleton import BOT
from bot.utils import escape, only_eagle

logger = logging.getLogger(__name__)


class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, Sequence("reminder_id_seq"), primary_key=True)
    what = Column(String)
    when = Column(DateTime)
    chat = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


REMINDME_WHAT = 0
REMINDME_WHAT_ID = "remindme_what"
REMINDME_WHAT_QUESTION = "remindme_what_question"

@only_eagle
def remindme(update: Update, ctx: CallbackContext) -> int:
    if len(ctx.args) == 0:
        update.message.reply_text(
            f"Devi usarlo così cara: /remindme <data>",
            quote=True,
        )
        return ConversationHandler.END

    when = " ".join(ctx.args)

    when = dateparser.parse(when, languages=["it"])
    if when is None:
        update.message.reply_text(
            f"Mi dispiace cara, ma questa non mi sembra una data!",
            quote=True,
        )
        return ConversationHandler.END

    if when <= datetime.now():
        update.message.reply_text(
            f"Mi dispiace cara, ma non posso ricordarti cose nel passato!",
            quote=True,
        )
        return ConversationHandler.END

    question = update.message.reply_text(
        f"Ok cara, cosa ti devo ricordare il {when.strftime('%d/%m/%Y')} alle {when.strftime('%H:%M')}??\n\nRispondi /cancel per annullare.",
        quote=True,
        reply_markup=ForceReply(selective=True, input_field_placeholder="Comprare il latte..."),
    )
    ctx.user_data[REMINDME_WHAT_QUESTION] = question

    return REMINDME_WHAT


def remindme_what(update: Update, ctx: CallbackContext) -> int:
    when = ctx.user_data[REMINDME_WHAT_ID]
    what = update.message.text
    chat = update.effective_chat.id

    ctx.user_data[REMINDME_WHAT_QUESTION].delete()

    try:
        with Session() as session:
            reminder = Reminder(what=what, when=when, chat=chat)
            session.add(reminder)
            session.commit()
            scheduler.add_job(remind, "date", [reminder.id], run_date=when)
    except Exception as err:
        logger.error(err)
        update.message.reply_text(
            f"Mi dispiace cara, ma non posso ricordarti questo!",
            quote=True,
        )
        return ConversationHandler.END

    update.message.reply_text(
        f"Ok cara, ti ricorderò di \"{what}\" il {when.strftime('%Y/%m/%d')} alle {when.strftime('%H:%M')}",
        quote=True,
    )

    return ConversationHandler.END

@only_eagle
def reminders(update: Update, _: CallbackContext) -> None:
    chat = update.effective_chat.id
    with Session() as session:
        reminders = (
            session.query(Reminder)
            .filter_by(chat=chat)
            .filter(Reminder.when > datetime.now())
            .order_by(Reminder.when.desc())
            .all()
        )
    reminders_txt = "\n\n".join(
        [
            f"📝 *{escape(reminder.what)}*\n"
            + f"⏰ {escape(reminder.when.strftime('%Y/%m/%d'))} alle {escape(reminder.when.strftime('%H:%M'))}"
            for reminder in reminders
        ]
    )
    update.message.reply_markdown_v2(
        f"Ti sto ricordando {len(reminders)} cose\.\n\n{reminders_txt}",
        quote=True,
    )


def remind(id: int) -> None:
    with Session() as session:
        reminder = session.query(Reminder).filter_by(id=id).first()
        BOT.send_message(reminder.chat, f"{reminder.what}")
        session.delete(reminder)
        session.commit()


def cancel(update: Update, ctx: CallbackContext) -> int:
    ctx.user_data[REMINDME_WHAT_QUESTION].delete()
    update.message.reply_text(f"Ok cara, parleremo più tardi...", quote=True)

    return ConversationHandler.END


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("remindme", remindme)],
            states={
                REMINDME_WHAT: [
                    MessageHandler(Filters.text & ~Filters.command, remindme_what)
                ],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
    )
    dispatcher.add_handler(CommandHandler("reminders", reminders))
