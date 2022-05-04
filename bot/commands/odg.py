from sqlalchemy import Column, DateTime, Integer, Sequence, String, func

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler

from bot.database.base import Base
from bot.database.session import Session
from bot.utils import escape, only_eagle


class Odg(Base):
    __tablename__ = "odg"
    id = Column(Integer, Sequence("odg_id_seq"), primary_key=True)
    what = Column(String)
    chat = Column(Integer)
    creator = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


@only_eagle
def odg(update: Update, ctx: CallbackContext):
    chat = update.effective_chat.id
    if len(ctx.args) == 1 and ctx.args[0] == "reset":
        with Session() as session:
            session.query(Odg).filter_by(chat=chat).delete()
            session.commit()

        update.message.reply_text(
            f"Ok cara, ho cancellato l'ODG",
            quote=True,
        )
        return

    if len(ctx.args) == 0:
        with Session() as session:
            odg = (
                session.query(Odg)
                .filter_by(chat=chat)
                .order_by(Odg.time_created.desc())
                .all()
            )
        odg_txt = "\n\n".join(
            [f"📝 *{escape(item.what)}*\n" + f"👤 {escape(item.creator)}" for item in odg]
        )
        update.message.reply_markdown_v2(
            f"L'ODG conta {len(odg)} cose\.\n\n{odg_txt}",
            quote=True,
        )
        return

    what = " ".join(ctx.args)

    creator = update.effective_user.full_name

    with Session() as session:
        odg = Odg(what=what, chat=chat, creator=creator)
        session.add(odg)
        session.commit()

    update.message.reply_text(
        f'Ok cara, ho aggiunto "{what}" all\'ODG',
        quote=True,
    )


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("odg", odg))
