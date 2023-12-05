from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError

from app.app import app


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Change here to Logger
    return JSONResponse(
        status_code=422,
        content={
            "detail": f"{exc.errors()[0]['loc'][-1]} alanında hata oluştu.",
            "extra": repr(exc),
        },
    )


@app.exception_handler(DuplicateKeyError)
async def duplicate_exception_handler(request: Request, exc: DuplicateKeyError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": f"{exc.details['keyValue']} kaydı zaten mevcut.",
            "extra": repr(exc),
        },
    )
