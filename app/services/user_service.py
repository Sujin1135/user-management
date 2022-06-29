import bcrypt

from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate


class UserService:
    def create(self, data: UserCreate):
        data.password = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        return crud_user.create(data)
