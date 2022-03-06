import functools
from typing import Any, Callable

from telegram import Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown

from bot import config


def sudo(
    fn: Callable[[Update, CallbackContext], None]
) -> Callable[[Update, CallbackContext], None]:
    @functools.wraps(fn)
    def callback(update: Update, ctx: CallbackContext):
        user = update.effective_user
        if user.id == config.ADMIN:
            fn(update, ctx)

    return callback


def only_eagle(
    fn: Callable[[Update, CallbackContext], None]
) -> Callable[[Update, CallbackContext], None]:
    @functools.wraps(fn)
    def callback(update: Update, ctx: CallbackContext):
        chat = update.effective_chat
        if chat.id in config.EAGLE:
            return fn(update, ctx)
        return None

    return callback


def escape(anything: Any) -> str:
    return escape_markdown(str(anything), version=2)
