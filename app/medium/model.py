import requests
from datetime import datetime
from random import randint
from traceback import format_exc

from pydantic import Field
from pymongo import IndexModel

from app.mixins.general import BaseDocument
from app.mixins.posts import PostMixin
from app.general.logger import logger


class MediumPost(PostMixin, BaseDocument):
    __title__ = "Medium"
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

    


class Medium(BaseDocument):
    active: bool = Field(title="Aktif", default=True)
    name: str | None = Field(title="İsim", default="")
    account_id: str = Field(title="Hesap ID", default="")
    access_token: str = Field(title="AccessToken", default="")

    def get_acc_id(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "application/json",
        }
        url = 'https://api.medium.com/v1/me'
        response = requests.get(url, headers=headers)
        return response.json()["data"]["id"]

    def send_post(self, details: MediumPost):
        payload = {
            "title": details.title,
            "contentFormat": "html",
            "content": f"<h1>{details.title}</h1><p>{details.desc}</p>",
            "tags": details.tags,
            "canonicalUrl": details.blogURL,
            "publishStatus": "public",
        }
           
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        url = f"https://api.medium.com/v1/users/{self.account_id}/posts"
        response = requests.request("POST", url, json=payload, headers=headers)
        logger.info(f'Medium Post response: {vars(response)}')
        return response.json()

    @classmethod
    async def send_random_post(cls):
        post = await MediumPost.random()
        accout = await cls.random()
        if not accout:
            return False
        try:
            res = accout.send_post(post)
            logger.info('Medium Post result:')
            logger.info(res)
            sent_url = res["data"]["url"]
            await post.set(
                {MediumPost.sent: True, MediumPost.sentDate: datetime.now(), MediumPost.sentURL: sent_url, MediumPost.sentAccout: accout.name}
            )
            logger.info(f'Medium Post sent: {sent_url}')
            return res
        except Exception as e:
            logger.error('Medium Error:', exc_info=True)
