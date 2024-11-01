from sqlalchemy import Column, Integer, String
from telegram import Update
from telegram.ext import (
    Dispatcher,
    CallbackContext,
    MessageHandler,
)
from bot.database.base import Base
from bot.database.session import Session

from telegram.ext import filters as Filters

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    username = Column(String)


def tracker(update: Update, _: CallbackContext):
    with Session() as session:
        user = User(
            id=update.effective_user.id,
            full_name=update.effective_user.full_name,
            username=update.effective_user.username,
        )
        session.merge(user)


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, tracker))
