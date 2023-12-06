from fastapi import FastAPI

from app.general.router import router as general_router
from app.twitter.router import router as twitter_router
from app.rss.router import router as rss_router

app = FastAPI()
app.include_router(general_router)
app.include_router(twitter_router, tags=["Twitter"], prefix="/twitter")
app.include_router(rss_router, tags=["RSS"], prefix="/rss")
