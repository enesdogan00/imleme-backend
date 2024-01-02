from random import randint
from beanie import Link
from pydantic import BaseModel

from app.rss.model import RSS

class PostMixin(BaseModel):
    rss_id: Link[RSS]
    @classmethod
    async def random(cls):
        count = await cls.find(cls.sent == False).count()
        random_index = randint(0, count - 1)
        random_document = (
            await cls.find(cls.sent == False).skip(random_index).limit(1).to_list(1)
        )[0]
        await random_document.fetch_link(cls.rss_id)
        feed = random_document.rss_id
        print(feed.daily_count)
        return random_document
