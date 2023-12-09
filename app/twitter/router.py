from beanie import PydanticObjectId
from fastapi import APIRouter

from app.general.constants import Success
from app.general.model import BaseResponse
from app.twitter.model import Twitter, TwitterPost

router = APIRouter()


@router.get("/account")
async def get_twitter_account() -> list[Twitter]:
    return await Twitter.find().to_list()


@router.post("/account")
async def create_twitter_account(data: Twitter) -> BaseResponse:
    await data.save()
    return BaseResponse(data=data, message=Success.created)


@router.delete("/account/{id}")
async def delete_twitter_account(id: PydanticObjectId) -> BaseResponse:
    await Twitter.find_one(Twitter.id == id).delete()
    return BaseResponse(message=Success.deleted)


@router.get("/post")
async def get_twitter_post() -> list[TwitterPost]:
    return await TwitterPost.find().limit(100).sort("-date").to_list()


@router.post("/post")
async def create_twitter_post(data: TwitterPost) -> BaseResponse:
    await data.save()
    return BaseResponse(data=data, message=Success.created)


@router.delete("/post/{id}")
async def delete_twitter_post(id: PydanticObjectId) -> BaseResponse:
    await TwitterPost.find_one(TwitterPost.id == id).delete()
    return BaseResponse(message=Success.deleted)
