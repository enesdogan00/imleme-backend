from decouple import config
from fastapi.openapi.utils import get_openapi
from fastapi_utilities import repeat_every

from app.app import app
from app.database import init_db
from app.folkd.model import Folkd
from app.rss.model import RSS
from app.twitter.model import Twitter


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="İmleme",
        version="0.0.1",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.on_event("startup")
async def startup():
    await init_db()
    app.openapi = custom_openapi


@app.on_event("startup")
@repeat_every(seconds=int(config("POST_INT", 120)))
async def send_random_post():
    classes = [Twitter, Folkd]
    for cls in classes:
        try:
            await cls.send_random_post()
        except Exception as e:
            print(e)


@app.on_event("startup")
@repeat_every(seconds=int(config("POST_INT", 120)))
async def rss_to_twitter():
    feeds = await RSS.find().to_list()
    for feed in feeds:
        try:
            await feed.feed_to_twitter()
        except:
            pass  # TODO: add logging

@app.on_event("startup")
@repeat_every(seconds=int(config("POST_INT", 120)))
async def rss_to_folkd():
    feeds = await RSS.find().to_list()
    for feed in feeds:
        try:
            await feed.feed_to_folkd()
        except Exception as e:
            pass

@app.on_event("startup")
@repeat_every(seconds=int(config("POST_INT", 120)))
async def rss_to_medium():
    feeds = await RSS.find().to_list()
    for feed in feeds:
        try:
            await feed.feed_to_medium()
        except Exception as e:
            pass