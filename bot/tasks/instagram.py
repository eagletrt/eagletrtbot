import os

from instagrapi import Client
from instagrapi.types import Media

from sqlalchemy import Column, Integer, Sequence
from telegram import InputMediaPhoto, InputMediaVideo

from bot import config
from bot.database.session import Session
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
    caption = media.caption_text # TODO: add link
    if media.media_type == PHOTO:
        BOT.send_photo(config.SPAM, media.thumbnail_url, caption=caption)
    elif media.media_type == VIDEO:
        BOT.send_video(config.SPAM, media.video_url, caption=caption)
    elif media.media_type == ALBUM:
        if len(media.resources) > 10:
            media.resources = media.resources[:10]
        resources = [
            InputMediaPhoto(resource.thumbnail_url)
            if resource.media_type == PHOTO
            else InputMediaVideo(resource.video_url)
            for resource in media.resources
        ]
        resources[0].caption = caption
        BOT.send_media_group(config.SPAM, resources)


def task():
    cl = Client()
    if os.path.exists("instagram.json"):
        cl.load_settings("instagram.json")
    cl.login("eagletrt", os.environ["INSTAGRAM_PASSWORD"])
    cl.dump_settings("instagram.json")
    medias = cl.user_medias(cl.user_id, amount=1)

    with Session() as session:
        empty = session.query(InstagramMedia).count() == 0 # prevent flood on first start
        for media in medias:
            if session.query(InstagramMedia).filter_by(instagram_id=media.id).count() == 0:
                if not empty:
                    send_media(media)
                session.add(InstagramMedia(instagram_id=media.id))
        session.commit()
