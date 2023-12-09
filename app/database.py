from datetime import timedelta
from secrets import token_urlsafe

from beanie import init_beanie
from decouple import config
from fastapi_jwt import JwtAccessBearer

from app.rss.model import RSS
from app.twitter.model import Twitter, TwitterPost

access_security = JwtAccessBearer(
    secret_key=token_urlsafe(32),
    auto_error=True,
    access_expires_delta=timedelta(days=2),
)


async def init_db():
    # TODO: init all app.modeldynamically
    await init_beanie(
        connection_string=config("MONGO_URI"),
        document_models=[
            Twitter,
            TwitterPost,
            RSS,
        ],
        recreate_views=True,
    )
