from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str = Field(title="email", max_length=50)
    password: str = Field(title="password", min_length=8, max_length=16)
    nickname: str = Field(title="nickname", min_length=2, max_length=50)
    name: str = Field(title="name", min_length=2, max_length=50)
    phone_number: str = Field(title="phone_number", max_length=15)


class UserUpdate(BaseModel):
    id: int = Field(title="id", ge=1)
    email: Optional[str] = Field(title="email", max_length=50)
    password: Optional[str] = Field(title="password", min_length=8, max_length=16)
    nickname: Optional[str] = Field(title="nickname", min_length=2, max_length=50)
    name: Optional[str] = Field(title="name", min_length=2, max_length=50)
    phone_number: Optional[str] = Field(title="phone_number", max_length=15)