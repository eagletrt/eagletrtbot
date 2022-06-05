import os

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


class TikTokMedia(Base):
    __tablename__ = "tiktok_media"
    id = Column(Integer, Sequence("tiktok_media_id_seq"), primary_key=True)
    tiktok_id = Column(Integer)


# def send_media(media: Media):
#     caption = media.caption_text
#     url = f"https://www.instagram.com/p/{media.code}"
#     text = f"{caption}\n\n🌐 {url}"
#     if media.media_type == PHOTO:
#         BOT.send_photo(config.SPAM, media.thumbnail_url, caption=text)
#     elif media.media_type == VIDEO:
#         BOT.send_video(config.SPAM, media.video_url, caption=text)
#     elif media.media_type == ALBUM:
#         if len(media.resources) > 10:
#             media.resources = media.resources[:10]
#         resources = [
#             InputMediaPhoto(resource.thumbnail_url)
#             if resource.media_type == PHOTO
#             else InputMediaVideo(resource.video_url)
#             for resource in media.resources
#         ]
#         resources[0].caption = text
#         BOT.send_media_group(config.SPAM, resources)
#     with open(LIKE_AND_SAVE, "rb") as sticker:
#         BOT.send_sticker(config.SPAM, sticker)


def task():
    if os.environ.get("NO_TIK_TOK", None) is not None:
        print("TikTok task didn't run because NO_TIK_TOK was set in env")
        return

    cl = Client()

    try:
        if os.path.exists("data/instagram.json"):
            cl.load_settings("data/instagram.json")
        cl.login("eagletrt", os.environ["INSTAGRAM_PASSWORD"])
        if not os.path.exists("data/instagram.json"):
            cl.dump_settings("data/instagram.json")
        cl.get_timeline_feed()
    except Exception as error:
        print(error)
        print("instagram login failed")
        return

if __name__ == "__main__":
    task()