from datetime import datetime
from random import randint
from traceback import format_exc

from folkd import Folkd as FolkdClient
from folkd import Post
from pydantic import Field
from pymongo import IndexModel

from app.mixins.general import BaseDocument
from app.mixins.posts import PostMixin


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

    


class Folkd(BaseDocument):
    active: bool = Field(title="Aktif", default=True)
    name: str | None = Field(title="İsim", default="")
    email: str = Field(title="Email")
    password: str = Field(title="Password")

    def send_post(self, details: Post):
        try:
            client = FolkdClient(self.email,self.password, headless=True)
        except Exception as e:
            print(e)
            st = format_exc()
            print(st)
            return False
        finally:
            client.driver.quit()

        res = client.send_post(details)
        return res

    @classmethod
    async def send_random_post(cls):
        post = await FolkdPost.random()
        accout = await cls.random()
        try:
            details = Post(
                url=post.blogURL,
                title=post.title,
                desc=post.desc,
                tags=post.tags
            )
            res = accout.send_post(details)
            if res:
                await post.set(
                    {FolkdPost.sent: True, FolkdPost.sentDate: datetime.now(), FolkdPost.sentAccout: accout.name, FolkdPost.sentURL: res}
                )
                return res
        except Exception as e:
            print(e)
            st = format_exc()
            print(st)
            return False
