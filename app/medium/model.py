import requests
from datetime import datetime
from random import randint
from traceback import format_exc

from pydantic import Field
from pymongo import IndexModel

from app.mixins.general import BaseDocument


class MediumPost(BaseDocument):
    __title__ = "Medium"
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


class Medium(BaseDocument):
    active: bool = Field(title="Aktif", default=True)
    name: str | None = Field(title="İsim", default="")
    account_id: str = Field(title="Hesap ID", default="")
    access_token: str = Field(title="AccessToken", default="")

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
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        url = f"https://api.medium.com/v1/users/{self.account_id}/posts"

        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.json())
        return response.json()
    async def get_acc_id(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.request("GET", 'https://api.medium.com/v1/me', headers=headers)
        self.account_id = response.json()["data"]["id"]
        return True

    @classmethod
    async def send_random_post(cls):
        post = await MediumPost.random()
        accout = await cls.random()
        try:
            res = accout.send_post(post)
            print(res)
            await post.set(
                {MediumPost.sent: True, MediumPost.sentDate: datetime.now(), MediumPost.sentURL: res["data"]["url"], MediumPost.sentAccout: accout.name}
            )
            return res
        except Exception as e:
            print(e)
            return False
