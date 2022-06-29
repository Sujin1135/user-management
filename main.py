from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

from app.api.v1.api import v1_router
from app.exceptions.duplication_error import DuplicationError
from app.exceptions.not_found_error import NotFoundError

app = FastAPI()


@app.exception_handler(ValueError)
async def validation_handler(_, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.args[0]},
    )


@app.exception_handler(DuplicationError)
async def duplication_handler(_, exc: DuplicationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.args[0]},
    )


@app.exception_handler(NotFoundError)
async def not_found_handler(_, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.args[0]},
    )


app.include_router(v1_router, tags=["v1"], prefix="/api/v1")
