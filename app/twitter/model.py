from datetime import datetime
from random import randint
from pymongo import IndexModel
import tweepy

from pydantic import Field

from app.mixins.general import BaseDocument


class TwitterPost(BaseDocument):
    __title__ = "Twitter"
    text: str = Field(title="Tweet İçeriği", default="")
    date: datetime | None = Field(default_factory=datetime.now)
    website: str = Field( default="")
    sent: bool = Field(default=False)
    sentDate: datetime | None = Field(title="Gönderim Tarihi", default_factory=datetime.now)

    class Settings:
        indexes = [
            IndexModel(
                [("text", 1)],
                unique=True,
            ),
        ]

    @classmethod
    async def random(cls):
        count = await cls.find(cls.sent == False).count()
        random_index = randint(0, count - 1)
        random_document = (
            await cls.find(cls.sent == False).skip(random_index).limit(1).to_list(1)
        )
        return random_document[0]


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
        try:
            res = accout.send_post(post.text)
            print(res)
            await post.set({TwitterPost.sent: True, TwitterPost.sentTime: datetime.now()})
            return res
        except Exception as e:
            print(e)
            return False
