from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get(
    "/", include_in_schema=False
)  # include_in_schema=False to hide it from the docs
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
