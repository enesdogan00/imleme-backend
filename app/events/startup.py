from decouple import config
from fastapi.openapi.utils import get_openapi
from fastapi_utilities import repeat_every
from app.app import app
from app.database import init_db
from app.twitter.model import Twitter


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Forza Otomasyon",
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
@repeat_every(seconds=config("POST_INT", 60))  # TODO: make this env
async def send_random_post():
    classes = [Twitter]
    for cls in classes:
        await cls.send_random_post()