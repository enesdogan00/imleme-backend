from beanie import PydanticObjectId
from fastapi import APIRouter

from app.folkd.model import Folkd, FolkdPost
from app.general.constants import Success
from app.general.model import BaseResponse

router = APIRouter()


@router.get("/account")
async def get_folkd_account() -> list[Folkd]:
    return await Folkd.find().to_list()


@router.post("/account")
async def create_folkd_account(data: Folkd) -> BaseResponse:
    await data.save()
    return BaseResponse(data=data, message=Success.created)


@router.delete("/account/{id}")
async def delete_folkd_account(id: PydanticObjectId) -> BaseResponse:
    await Folkd.find_one(Folkd.id == id).delete()
    return BaseResponse(message=Success.deleted)


@router.get("/post")
async def get_folkd_post() -> list[FolkdPost]:
    return await FolkdPost.find().limit(100).sort("-date").to_list()


@router.post("/post")
async def create_folkd_post(data: FolkdPost) -> BaseResponse:
    await data.save()
    return BaseResponse(data=data, message=Success.created)


@router.delete("/post/{id}")
async def delete_folkd_post(id: PydanticObjectId) -> BaseResponse:
    await FolkdPost.find_one(FolkdPost.id == id).delete()
    return BaseResponse(message=Success.deleted)
