from fastapi.openapi.utils import get_openapi

from app.app import app
from app.database import init_db


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
