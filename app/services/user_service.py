import bcrypt

from app.core.auth import create_access_token
from app.crud.crud_user import crud_user
from app.exceptions.unauthorized_error import UnauthorizedError
from app.schemas.login_tokens import LoginTokens
from app.schemas.user import UserCreate

ENCODE_TYPE = "utf-8"


class UserService:
    def create(self, data: UserCreate):
        data.password = bcrypt.hashpw(
            data.password.encode(ENCODE_TYPE), bcrypt.gensalt()
        ).decode(ENCODE_TYPE)
        return crud_user.create(data)

    def verify_password(self, email: str, password: str):
        is_valid = bcrypt.checkpw(
            password.encode(ENCODE_TYPE),
            crud_user.get_by_email(email).password.encode(ENCODE_TYPE),
        )
        if not is_valid:
            raise UnauthorizedError()

        return True

    def login(self, email: str, password: str):
        self.verify_password(email, password)

        return LoginTokens(access_token=create_access_token(email))
