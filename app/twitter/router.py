from fastapi import APIRouter

from app.general.constants import Success
from app.general.model import BaseResponse
from app.twitter.model import Twitter, TwitterPost

router = APIRouter()

@router.post("/account")
async def create_twitter_account(data: Twitter) -> BaseResponse:
    await data.save()
    return BaseResponse(data=data, message=Success.created)

@router.post("/post")
async def create_twitter_post(data: TwitterPost) -> BaseResponse:
    await data.save()
    return BaseResponse(data=data, message=Success.created)
