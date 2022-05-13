from datetime import datetime
from io import BytesIO
from PIL import ImageDraw
from sqlalchemy import Column, DateTime, Integer, Sequence, desc

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, CommandHandler

from bot.database.base import Base
from bot.database.session import Session

from bot.media import DAY_SINCE_FIRE, FONT_XL
from bot.utils import only_eagle


class Fires(Base):
    __tablename__ = "fires"
    id = Column(Integer, Sequence("fires_id_seq"), primary_key=True)
    when = Column(DateTime)


@only_eagle
def fire(update: Update, ctx: CallbackContext):
    if len(ctx.args) == 1 and ctx.args[0] == "reset":
        with Session() as session:
            reminder = Fires(when=datetime.now())
            session.add(reminder)
            session.commit()

    image = DAY_SINCE_FIRE.copy()

    with Session() as session:
        fire = session.query(Fires).order_by(Fires.when.desc()).first()
        if fire:
            delta = (datetime.now() - fire.when).days
        else:
            delta = 999

    delta = str(delta).rjust(3, "0")
    a, b, c = delta[0], delta[1], delta[2]

    draw = ImageDraw.Draw(image)
    draw.text((280, 610), a, font=FONT_XL, fill=(0, 0, 0, 255))
    draw.text((460, 610), b, font=FONT_XL, fill=(0, 0, 0, 255))
    draw.text((640, 610), c, font=FONT_XL, fill=(0, 0, 0, 255))

    bio = BytesIO()
    bio.name = "meme.webp"
    image.save(bio, "WEBP")
    bio.seek(0)

    update.message.reply_sticker(bio)

    image.close()
    bio.close()


def register(dispatcher: Dispatcher[CallbackContext, dict, dict, dict]):
    dispatcher.add_handler(CommandHandler("fire", fire))
