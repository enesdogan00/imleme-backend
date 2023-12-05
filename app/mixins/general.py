from random import randint
from beanie import Document



class BaseDocument(Document):
    @classmethod
    async def random(cls):
        count = await cls.count()
        random_index = randint(0, count - 1)
        random_document = await cls.find().skip(random_index).limit(1).to_list(1)
        return random_document[0]
