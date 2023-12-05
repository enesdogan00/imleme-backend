from starlette_context.middleware import RawContextMiddleware

from app.app import app

app.add_middleware(RawContextMiddleware)
