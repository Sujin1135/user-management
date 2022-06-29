from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate, UserUpdate, UserRes
from app.services.user_service import UserService

router = APIRouter()
service = UserService()


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRes,
)
async def create(user: UserCreate = Body(...)):
    created = service.create(user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(
            UserRes(
                id=created.id,
                email=created.email,
                nickname=created.nickname,
                name=created.name,
                phone_number=created.phone_number,
                created_at=created.created_at,
                updated_at=created.updated_at,
                deleted_at=created.deleted_at,
            )
        ),
    )


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRes,
)
async def update(user_id: int, user: UserUpdate = Body(...)):
    crud_user.update(user_id, user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(UserRes(*crud_user.get(user_id))),
    )
