import functools
import re
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


re_emojis = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002500-\U00002BEF"  # chinese char
    "\U00002702-\U000027B0"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # dingbats
    "\u3030"
    "]+",
    flags=re.UNICODE,
)

re_command = re.compile("/[a-zA-Z@]+")
