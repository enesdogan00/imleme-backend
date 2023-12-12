from datetime import datetime
from random import randint

from folkd import Folkd as FolkdClient, Post
from pydantic import Field
from pymongo import IndexModel

from app.mixins.general import BaseDocument


class FolkdPost(BaseDocument):
    __title__ = "Folkd"
    blogURL: str | None = Field(default="", title="Blog Adresi")
    title: str = ""
    desc: str = ""
    tags: list[str] = Field(default=["Reklam", "Blog"],min_length=3)
    date: datetime | None = Field(default_factory=datetime.now)
    website: str = Field(default="")
    sent: bool = Field(default=False)
    sentDate: datetime | None = Field(
        title="Gönderim Tarihi", default_factory=datetime.now
    )
    sentURL: str | None = Field(default="", title="Gönderi Adresi")
    sentAccout: str | None = Field(default="", title="Gönderen Hesap")

    class Settings:
        indexes = [
            IndexModel(
                [("blogURL", 1)],
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


class Folkd(BaseDocument):
    active: bool = Field(title="Aktif", default=True)
    name: str | None = Field(title="İsim", default="")
    email: str = Field(title="Email")
    password: str = Field(title="Password")

    def send_post(self, text: str):
        client = FolkdClient(self.email,self.password)
        return client.send_post(text)

    @classmethod
    async def send_random_post(cls):
        post = await FolkdPost.random()
        accout = await cls.random()
        try:
            post = Post(
                url=post.blogURL,
                title=post.title,
                desc=post.desc,
                tags=post.tags
            )
            res = accout.send_post(post)
            print(res)
            await post.set(
                #TODO: add sent url
                {FolkdPost.sent: True, FolkdPost.sentDate: datetime.now(), FolkdPost.sentAccout: accout.name}
            )
            return res
        except Exception as e:
            print(e)
            return False
