from urllib.parse import urlparse

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, RedirectResponse
from app.rss.model import RSS

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
        {"$group": {"_id": "$rss_id", "count": {"$sum": 1}}},
    ]
    res = ""
    start_val = 1
    for cls in [TwitterPost, FolkdPost, MediumPost]:
        sites = await cls.aggregate(pipeline).to_list()
        for idx, site in enumerate(sites, start_val):
            feed = await RSS.get(site["_id"].id)                
            res += f"{idx}. {urlparse(feed.feed_url).netloc} {site['count']} adet {cls.__title__} post gönderildi." + "\n"
        
        start_val += len(sites)
    return PlainTextResponse(res)
