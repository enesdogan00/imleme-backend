from urllib.parse import urlparse

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, RedirectResponse

from app.twitter.model import TwitterPost
from app.folkd.model import FolkdPost
from app.medium.model import MediumPost

router = APIRouter()


@router.get(
    "/", include_in_schema=False
)  # include_in_schema=False to hide it from the docs
async def redirect_to_docs():
    return RedirectResponse(url="/api/docs")


@router.get("/dashboard")
async def dashboard() -> PlainTextResponse:
    pipeline = [
        {"$match": {"sent": True}},
        {"$group": {"_id": "$website", "count": {"$sum": 1}}},
    ]
    res = ""
    start_val = 1
    for cls in [TwitterPost, FolkdPost, MediumPost]:
        sites = await cls.aggregate(pipeline).to_list()
    
        res += "\n".join(
            [
                f"{idx}. {urlparse(site['_id']).netloc} {site['count']} adet {cls.__title__} post gönderildi."
                for idx, site in enumerate(sites, start_val)
            ]
        )
        start_val += len(sites)
        res += "\n"
    return PlainTextResponse(res)
