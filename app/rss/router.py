from beanie import PydanticObjectId
from fastapi import APIRouter

from app.general.constants import Success
from app.general.model import BaseResponse
from app.rss.model import RSS

router = APIRouter()


@router.get("/")
async def get_rss_feed() -> list[RSS]:
    return await RSS.find().to_list()


@router.get("/get_feed")
async def et_random_rss_feed():
    feed = await RSS.random()
    await feed.feed_to_twitter()
    return True


@router.post("/")
async def create_rss_feed(data: RSS) -> BaseResponse:
    await data.save()
    return BaseResponse(data=data, message=Success.created)


@router.post("/multiple")
async def create_rss_feed_multiple(data: list[str]) -> BaseResponse:
    await RSS.insert_many(RSS(feed_url=url) for url in data)
    return BaseResponse(data=data, message=Success.created)


@router.delete("/{id}")
async def delete_rss_feed(id: PydanticObjectId) -> BaseResponse:
    await RSS.find_one(RSS.id == id).delete()
    return BaseResponse(message=Success.deleted)
