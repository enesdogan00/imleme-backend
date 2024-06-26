from datetime import datetime
from random import randint
from traceback import format_exc

from folkd import Folkd as FolkdClient
from folkd import Post
from pydantic import Field
from pymongo import IndexModel

from app.mixins.general import BaseDocument
from app.mixins.posts import PostMixin
from app.general.logger import logger


class FolkdPost(PostMixin, BaseDocument):
    __title__ = "Folkd"
    blogURL: str | None = Field(default="", title="Blog Adresi")
    title: str = ""
    desc: str = ""
    tags: list[str] = Field(default=["Reklam", "Blog"],min_length=3)
    date: datetime | None = Field(default_factory=datetime.now)
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
    


class Folkd(BaseDocument):
    active: bool = Field(title="Aktif", default=True)
    name: str | None = Field(title="İsim", default="")
    email: str = Field(title="Email")
    password: str = Field(title="Password")

    def send_post(self, details: Post):
        try:
            client = FolkdClient(self.email,self.password, headless=True)
            res = client.send_post(details)
            client.driver.quit()
            return res
        except Exception as e:
            logger.error('Folkd Error:', exc_info=True)
        return False

    @classmethod
    async def send_random_post(cls):
        post = await FolkdPost.random()
        accout = await cls.random()
        if not accout:
            return False
        try:
            desc = post.desc
            while len(desc) <= 300:
                desc += " " + post.desc
            desc = desc[:900]
            details = Post(
                url=post.blogURL,
                title=post.title,
                desc=desc,
                tags=post.tags
            )
            res = accout.send_post(details)
            if res:
                await post.set(
                    {FolkdPost.sent: True, FolkdPost.sentDate: datetime.now(), FolkdPost.sentAccout: accout.name, FolkdPost.sentURL: res}
                )
                logger.info(f'Folkd Post Sent: {res}')
                return res
        except Exception as e:
            logger.error('Folkd Error:', exc_info=True)
            return False
