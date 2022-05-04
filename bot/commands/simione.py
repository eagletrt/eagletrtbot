from io import BytesIO
import textwrap
from PIL import ImageDraw

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler

from bot.media import SIMIONE, SIMIONE_FILE, FONT_MD
from bot.utils import only_eagle


@only_eagle
def simione(update: Update, ctx: CallbackContext):
    default = "SIMIONE!"

    if (
        update.message is not None
        and update.message.reply_to_message is not None
        and update.message.reply_to_message.text
    ):
        if len(update.message.reply_to_message.text) > 0:
            default = update.message.reply_to_message.text

    image = SIMIONE.copy()

    draw = ImageDraw.Draw(image)

    message = " ".join(ctx.args) if len(ctx.args) > 0 else default

    message = "\n".join(textwrap.wrap(message, width=20))

    draw.multiline_text(
        (870, 400),
        message,
        anchor="mm",
        align="center",
        font=FONT_MD,
        fill=(0, 0, 0, 255),
    )

    bio = BytesIO()
    bio.name = SIMIONE_FILE
    image.save(bio, "JPEG")
    bio.seek(0)

    update.message.reply_photo(bio)


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("simione", simione))
