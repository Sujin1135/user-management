from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.base import BaseRes


EMAIL_FIELD = Field(title="email", max_length=50)
PWD_FIELD = Field(title="password", min_length=8, max_length=16)
NICKNAME_FIELD = Field(title="nickname", max_length=50)
NAME_FIELD = Field(title="name", max_length=50)
PHONE_NUMBER_FIELD = Field(title="phone_number", max_length=15)


class UserCreate(BaseModel):
    email: str = EMAIL_FIELD
    password: str = PWD_FIELD
    nickname: str = NICKNAME_FIELD
    name: str = NAME_FIELD
    phone_number: str = PHONE_NUMBER_FIELD

    class Config:
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    id: int = Field(title="id", ge=1)
    email: Optional[str] = EMAIL_FIELD
    password: Optional[str] = PWD_FIELD
    nickname: Optional[str] = NICKNAME_FIELD
    name: Optional[str] = NAME_FIELD
    phone_number: Optional[str] = PHONE_NUMBER_FIELD

    class Config:
        arbitrary_types_allowed = True


class UserRes(BaseRes):
    id: int
    email: str
    nickname: str
    name: str
    phone_number: str


class LoginReq(BaseModel):
    email: str = EMAIL_FIELD
    password: str = PWD_FIELD


class UserPwdChange(BaseModel):
    current_password: str = PWD_FIELD
    change_password: str = PWD_FIELD
