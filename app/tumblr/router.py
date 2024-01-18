from beanie import PydanticObjectId
from fastapi import APIRouter
from app.rss.model import RSS

from app.tumblr.model import Tumblr, TumblrPost
from app.general.constants import Success
from app.general.model import BaseResponse

router = APIRouter()


@router.get("/account")
async def get_tumblr_account() -> list[Tumblr]:
    return await Tumblr.find().to_list()


@router.get("/account/auth_url")
async def get_tumblr_auth_url() -> str:
    return Tumblr.get_full_auth_url()


@router.post("/account")
async def create_tumblr_account(data: Tumblr) -> BaseResponse:
    await data.save()
    return BaseResponse(data=data, message=Success.created)

    
@router.get("/get_feed")
async def et_random_rss_feed():
    feed = await RSS.random()
    await feed.feed_to_tumblr()
    return True

@router.post("/post/test")
async def create_tumblr_account() -> BaseResponse:
    await Tumblr.send_random_post()
    return BaseResponse( message=Success.created)


@router.delete("/account/{id}")
async def delete_tumblr_account(id: PydanticObjectId) -> BaseResponse:
    await Tumblr.find_one(Tumblr.id == id).delete()
    return BaseResponse(message=Success.deleted)


@router.get("/post")
async def get_tumblr_post() -> list[TumblrPost]:
    return await TumblrPost.find().limit(100).sort("-date").to_list()


@router.post("/post")
async def create_tumblr_post(data: TumblrPost) -> BaseResponse:
    await data.save()
    return BaseResponse(data=data, message=Success.created)


@router.delete("/post/{id}")
async def delete_tumblr_post(id: PydanticObjectId) -> BaseResponse:
    await TumblrPost.find_one(TumblrPost.id == id).delete()
    return BaseResponse(message=Success.deleted)
