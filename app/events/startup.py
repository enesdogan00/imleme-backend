from traceback import format_exc
from decouple import config
from fastapi.openapi.utils import get_openapi
from fastapi_utilities import repeat_every

from app.app import app
from app.database import init_db
from app.folkd.model import Folkd
from app.medium.model import Medium
from app.rss.model import RSS
from app.twitter.model import Twitter
from app.general.logger import logger


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
    classes = [Twitter, Medium, Folkd]
    for cls in classes:
        try:
            await cls.send_random_post()
        except Exception as e:
            logger.error(f"{cls.__name__} Error:", exc_info=True)


@app.on_event("startup")
@repeat_every(seconds=int(config("POST_INT", 120)))
async def rss_to_twitter():
    feeds = await RSS.find().to_list()
    for feed in feeds:
        try:
            await feed.feed_to_twitter()
        except Exception as e:
            if all(err['code'] == 11000 for err in e.details.get("writeErrors", [{}])):
                return
            logger.error('RSS to Twitter Error:', exc_info=True)

@app.on_event("startup")
@repeat_every(seconds=int(config("POST_INT", 120)))
async def rss_to_folkd():
    feeds = await RSS.find().to_list()
    for feed in feeds:
        try:
            await feed.feed_to_folkd()
        except Exception as e:
            if all(err['code'] == 11000 for err in e.details.get("writeErrors", [{}])):
                return
            logger.error('RSS to Folkd Error:', exc_info=True)


@app.on_event("startup")
@repeat_every(seconds=int(config("POST_INT", 120)))
async def rss_to_medium():
    feeds = await RSS.find().to_list()
    for feed in feeds:
        try:
            await feed.feed_to_medium()
        except Exception as e:
            if all(err['code'] == 11000 for err in e.details.get("writeErrors", [{}])):
                return
            logger.error('RSS to Medium Error:', exc_info=True)