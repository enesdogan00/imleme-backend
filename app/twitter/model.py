from datetime import datetime
from random import randint
from traceback import format_exc

import tweepy
from pydantic import Field
from pymongo import IndexModel

from app.mixins.general import BaseDocument
from app.mixins.posts import PostMixin
from app.general.logger import logger


class TwitterPost(PostMixin, BaseDocument):
    __title__ = "Twitter"
    text: str = Field(title="Tweet İçeriği", default="")
    date: datetime | None = Field(default_factory=datetime.now)
    sent: bool = Field(default=False)
    sentDate: datetime | None = Field(
        title="Gönderim Tarihi", default_factory=datetime.now
    )
    sentURL: str | None = Field(default="", title="Gönderi Adresi")
    blogURL: str | None = Field(default="", title="Blog Adresi")
    sentAccout: str | None = Field(default="", title="Gönderen Hesap")

    class Settings:
        indexes = [
            IndexModel(
                [("text", 1)],
                unique=True,
            ),
        ]

    


class Twitter(BaseDocument):
    active: bool = Field(title="Aktif", default=True)
    name: str | None = Field(title="İsim", default="")
    consumer_key: str = Field(title="Consumer Key")
    consumer_secret: str = Field(title="Consumer Secret")
    access_token: str = Field(title="Access Token")
    access_token_secret: str = Field(title="Access Token Secret")

    def send_post(self, text: str):
        client = tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )
        return client.create_tweet(text=text)

    @classmethod
    async def send_random_post(cls):
        post = await TwitterPost.random()
        accout = await cls.random()
        if not accout:
            return False
        try:
            res = accout.send_post(post.text)
            logger.info('Twitter Post Reult:')
            logger.info(res)
            sent_url = f'https://twitter.com/{accout.name}/status/{res.data["id"]}'
            await post.set(
                {TwitterPost.sent: True, TwitterPost.sentDate: datetime.now(), TwitterPost.sentURL: sent_url, TwitterPost.sentAccout: accout.name}
            )
            logger.info(f'Twitter Post Sent: {sent_url}')
            return res
        except Exception as e:
            if not isinstance(e, tweepy.errors.TooManyRequests):
                logger.error(f'Twitter Error: {e}')
            return False
