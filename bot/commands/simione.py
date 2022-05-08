from io import BytesIO
import re
import textwrap
from typing import Tuple
from PIL import Image, ImageDraw, ImageOps

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler

from bot.media import SIMIONE, FONT_MD, VOLPONE
from bot.utils import only_eagle

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


@only_eagle
def simione(update: Update, ctx: CallbackContext):
    center = (870, 400)
    max_size = (460, 360)
    template = SIMIONE
    default = "SIMIONE!"
    send_template(update, ctx, template, center, max_size, default)


@only_eagle
def volpone(update: Update, ctx: CallbackContext):
    center = (370, 355)
    max_size = (666, 372)
    template = VOLPONE
    default = "VOLPONE!"
    send_template(update, ctx, template, center, max_size, default)


def send_template(
    update: Update,
    ctx: CallbackContext,
    template: Image,
    center: Tuple[int, int],
    max_size: Tuple[int, int],
    default: str,
):
    other_image = None

    if update.message is not None and update.message.reply_to_message is not None:
        if update.message.reply_to_message.photo is not None:
            if len(update.message.reply_to_message.photo) > 0:
                photo = update.message.reply_to_message.photo[-1]
                byte_array = BytesIO(photo.get_file().download_as_bytearray())
                other_image = Image.open(byte_array)
                default = ""
        if update.message.reply_to_message.text is not None:
            if len(update.message.reply_to_message.text) > 0:
                default = update.message.reply_to_message.text

    message = (
        re_command.sub(r"", update.message.text.strip())
        if len(ctx.args) > 0
        else default
    )

    image = template.copy()
    draw = ImageDraw.Draw(image)

    if len(message) >= 0:
        message = message.strip()  # clean start and end
        message = re_emojis.sub(r"", message)  # remove emojis
        message = "\n".join(textwrap.wrap(message, width=20, replace_whitespace=False))
        draw.multiline_text(
            center,
            message,
            anchor="mm",
            align="center",
            font=FONT_MD,
            fill=(0, 0, 0, 255),
        )

    if other_image is not None:
        other_image = ImageOps.contain(other_image, max_size)
        offset = (
            center[0] - other_image.width // 2,
            center[1] - other_image.height // 2,
        )
        image.paste(other_image, offset)
        other_image.close()

    bio = BytesIO()
    bio.name = "meme.jpg"
    image.save(bio, "JPEG")
    bio.seek(0)
    update.message.reply_photo(bio)

    image.close()
    bio.close()


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("simione", simione))
    dispatcher.add_handler(CommandHandler("volpone", volpone))
