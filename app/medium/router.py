from beanie import PydanticObjectId
from fastapi import APIRouter

from app.medium.model import Medium, MediumPost
from app.general.constants import Success
from app.general.model import BaseResponse

router = APIRouter()


@router.get("/account")
async def get_medium_account() -> list[Medium]:
    return await Medium.find().to_list()

@router.get("/test")
async def test():
    await Medium.send_random_post()


@router.post("/account")
async def create_medium_account(data: Medium) -> BaseResponse:
    data.account_id = data.get_acc_id()
    await data.save()
    return BaseResponse(data=data, message=Success.created)


@router.delete("/account/{id}")
async def delete_medium_account(id: PydanticObjectId) -> BaseResponse:
    await Medium.find_one(Medium.id == id).delete()
    return BaseResponse(message=Success.deleted)


@router.get("/post")
async def get_medium_post() -> list[MediumPost]:
    return await MediumPost.find().limit(100).sort("-date").to_list()


@router.post("/post")
async def create_medium_post(data: MediumPost) -> BaseResponse:
    await data.save()
    return BaseResponse(data=data, message=Success.created)


@router.delete("/post/{id}")
async def delete_medium_post(id: PydanticObjectId) -> BaseResponse:
    await MediumPost.find_one(MediumPost.id == id).delete()
    return BaseResponse(message=Success.deleted)
