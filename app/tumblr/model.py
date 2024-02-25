from datetime import datetime
from random import randint
from traceback import format_exc
from beanie import Insert, before_event

from decouple import config
from tumblr import TumblrClient
from pydantic import Field
from pymongo import IndexModel

from app.mixins.general import BaseDocument
from app.mixins.posts import PostMixin
from app.general.logger import logger


class TumblrPost(PostMixin, BaseDocument):
    __title__ = "Tumblr"
    blogURL: str | None = Field(default="", title="Blog Adresi")
    title: str = ""
    desc: str = ""
    date: datetime | None = Field(default_factory=datetime.now)
    sent: bool = Field(default=False)
    sentDate: datetime | None = Field(
        title="Gönderim Tarihi", default_factory=datetime.now
    )
    sentURL: str | None = Field(default="", title="Gönderi Adresi")
    sentAccout: str | None = Field(default="", title="Gönderen Hesap")


class Tumblr(BaseDocument):
    active: bool = Field(title="Aktif", default=True)
    name: str | None = Field(title="İsim", default="")
    verifier: str = ""


    @classmethod
    def get_full_auth_url(cls):
        client = TumblrClient( config("tumblr_consumer_key", "AX6AltfGeEHYPZoljvzarmFOw1E560j3BSg2lEn72n4ISnhr3A"),
                config("tumblr_consumer_secret", "K1vaUk6wWovqqROv4WH6MTcZLUy5gu4DyLOFqH75p3SvQOXbFF"))
        return client.get_full_auth_url()

    def send_post(self, details: dict):
        try:
            client = TumblrClient(
                config("tumblr_consumer_key", "AX6AltfGeEHYPZoljvzarmFOw1E560j3BSg2lEn72n4ISnhr3A"),
                config("tumblr_consumer_secret", "K1vaUk6wWovqqROv4WH6MTcZLUy5gu4DyLOFqH75p3SvQOXbFF")
            )
            client.create_client(self.verifier)
            return client.create_text_post(details["title"], details["desc"])
        except Exception as e:
            logger.error('Tumblr Error:', exc_info=True)


    @classmethod
    async def send_random_post(cls):
        post = await TumblrPost.random()
        accout = await cls.random()
        try:
            details = {
                "title": post.title,
                "desc": post.desc,
            }
            res = accout.send_post(details)
            if res:
                await post.set(
                    {TumblrPost.sent: True, TumblrPost.sentDate: datetime.now(), TumblrPost.sentAccout: accout.name, TumblrPost.sentURL: res}
                )
                return res
        except Exception as e:
            logger.error('Tumblr Error:', exc_info=True)
            return False
