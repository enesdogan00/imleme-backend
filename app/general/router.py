from urllib.parse import urlparse
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.twitter.model import TwitterPost

router = APIRouter()


@router.get(
    "/", include_in_schema=False
)  # include_in_schema=False to hide it from the docs
async def redirect_to_docs():
    return RedirectResponse(url="/api/docs")

@router.get("/dashboard")
async def dashboard() -> str:
    pipeline = [
        {
            "$match": 
                    {"sent": True}
            
        },
        {
            "$group": {
                "_id": "$website",
                "count": {"$sum": 1}
            }
        }
    ]
    sites = await TwitterPost.aggregate(pipeline).to_list()
    res = "\n".join([f"{idx}. {urlparse(site['_id']).netloc} {site['count']} adet Twitter post gönderildi." for idx,site in enumerate(sites,1)])
    return res