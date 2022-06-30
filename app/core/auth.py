from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, JWTError
from starlette import status

from app.configs.config import config
from app.crud.crud_user import crud_user
from app.models.user import User
from app.schemas.token_data import TokenData
from app.schemas.user import UserRes

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = config.jwt["secret_key"]
JWT_REFRESH_SECRET_KEY = config.jwt["refresh_secret_key"]

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    # ex = int(expires_delta.timestamp())
    # get_redis_db().set(f"{subject}_access_token", encoded_jwt, ex)
    return encoded_jwt


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def _convert_user_model_to_schema(model: User):
    return UserRes(
        id=model.id,
        email=model.email,
        nickname=model.nickname,
        name=model.name,
        phone_number=model.phone_number,
        created_at=model.created_at,
        updated_at=model.updated_at,
        deleted_at=model.deleted_at,
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(email=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = crud_user.get_by_email(token_data.email)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return _convert_user_model_to_schema(user)
