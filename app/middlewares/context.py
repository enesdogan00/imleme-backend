from starlette_context.middleware import RawContextMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.app import app

app.add_middleware(RawContextMiddleware)
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)