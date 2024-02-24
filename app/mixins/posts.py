from datetime import datetime
from random import randint
from beanie import Link
from pydantic import BaseModel

from app.rss.model import RSS

class PostMixin(BaseModel):
    rss_id: Link[RSS] = None
    @classmethod
    async def random(cls):
        pipeline = [
  {
    "$match": {
      "sent": False
    }
  },
  {
    "$group": {
      "_id": "$rss_id",
      "count": { "$sum": 1 }
    }
  },
  {
    "$sort": {
      "count": -1
    }
  },
  {
    "$limit": 10
  },
   {"$sample": {"size": 1}}
]
        random_rss = (
            await cls.aggregate(pipeline).to_list()
        )
        if not random_rss:
            return None
        random_rss = random_rss[0]["_id"]
        random_document = await cls.aggregate([{"$match": {"rss_id": random_rss}}, {"$sample": {"size": 1}}]).to_list(1)
        random_document = random_document[0]
        random_document = await cls.get(random_document["_id"])
        return random_document
