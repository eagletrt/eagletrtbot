import os

from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from instagrapi.types import Media

from sqlalchemy import Column, Integer, Sequence
from telegram import InputMediaPhoto, InputMediaVideo

from bot import config
from bot.database.session import Session
from bot.media import LIKE_AND_SAVE
from bot.singleton import BOT
from bot.database.base import Base

PHOTO = 1
VIDEO = 2
ALBUM = 8


class InstagramMedia(Base):
    __tablename__ = "instagram_media"
    id = Column(Integer, Sequence("instagram_media_id_seq"), primary_key=True)
    instagram_id = Column(Integer)


def send_media(media: Media):
    caption = media.caption_text
    url = f"https://www.instagram.com/p/{media.code}"
    text = f"{caption}\n\n🌐 {url}"
    if media.media_type == PHOTO:
        BOT.send_photo(config.SPAM, media.thumbnail_url, caption=text)
    elif media.media_type == VIDEO:
        BOT.send_video(config.SPAM, media.video_url, caption=text)
    elif media.media_type == ALBUM:
        if len(media.resources) > 10:
            media.resources = media.resources[:10]
        resources = [
            InputMediaPhoto(resource.thumbnail_url)
            if resource.media_type == PHOTO
            else InputMediaVideo(resource.video_url)
            for resource in media.resources
        ]
        resources[0].caption = text
        BOT.send_media_group(config.SPAM, resources)
    with open(LIKE_AND_SAVE, "rb") as sticker:
        BOT.send_sticker(config.SPAM, sticker)

        
def handle_exception(client: Client, error: Exception):
    if isinstance(error, LoginRequired):
        print(error)
        client.relogin()
        return 
    raise error

def task():
    if os.environ.get("NO_INSTAGRAM", None) is not None:
        print("Instagram task didn't run because NO_INSTAGRAM was set in env")
        return

    cl = Client()
    cl.handle_exception = handle_exception

    try:
        if os.path.exists("data/instagram.json"):
            cl.load_settings("data/instagram.json")
        cl.login("eagletrt", os.environ["INSTAGRAM_PASSWORD"])
        cl.get_timeline_feed()
    except Exception as error:
        print(error)
        print("instagram login failed")
        return

    if not os.path.exists("data/instagram.json"):
        cl.dump_settings("data/instagram.json")

    medias = cl.user_medias(cl.user_id, amount=1)

    with Session() as session:
        empty = (
            session.query(InstagramMedia).count() == 0
        )  # prevent flood on first start
        for media in medias:
            if (
                session.query(InstagramMedia).filter_by(instagram_id=media.id).count()
                == 0
            ):
                session.add(InstagramMedia(instagram_id=media.id))
                session.commit()
                if not empty:
                    send_media(media)
