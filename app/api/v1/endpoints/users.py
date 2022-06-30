from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.core.auth import get_current_user
from app.schemas.login_tokens import LoginTokens
from app.schemas.user import UserCreate, UserRes, LoginReq, UserPwdChange
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


@router.post(
    "/signin",
    status_code=status.HTTP_200_OK,
    response_model=LoginTokens,
)
async def login(login_req: LoginReq):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(service.login(login_req.email, login_req.password)),
    )


async def get_current_active_user(current_user: UserRes = Depends(get_current_user)):
    if current_user.deleted_at:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/me", response_model=UserRes)
async def read_users_me(current_user: UserRes = Depends(get_current_active_user)):
    return current_user


@router.patch(
    "/me/change-pwd",
    status_code=status.HTTP_200_OK,
    response_model=UserRes,
)
async def change_password(
    current_user: UserRes = Depends(get_current_user),
    change_data: UserPwdChange = Body(...),
):
    service.change_pwd(current_user, change_data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(current_user),
    )
