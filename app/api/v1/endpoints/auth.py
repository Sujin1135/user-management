from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.crud.crud_user import crud_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def create(user: UserCreate = Body(...)):
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(crud_user.create(user)),
    )


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
)
async def update(user_id: int, user: UserUpdate = Body(...)):
    crud_user.update(user_id, user)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder(crud_user.get(user_id))
    )
