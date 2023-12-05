from fastapi import Request
from starlette_context import context

from app.app import app


@app.middleware("http")
async def auth(request: Request, call_next):
    if request.url.path.endswith(("login", "docs", "openapi.json")):
        return await call_next(request)

    context["SchoolCode"] = 1
    context["role"] = "student"
    return await call_next(request)
