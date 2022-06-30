from app.core.auth import (
    create_access_token,
    gen_hashed_password,
    compare_hashed_and_password,
)
from app.crud.crud_user import crud_user
from app.exceptions.unauthorized_error import UnauthorizedError
from app.schemas.login_tokens import LoginTokens
from app.schemas.user import UserCreate, UserPwdChange, UserRes


class UserService:
    def create(self, data: UserCreate):
        data.password = gen_hashed_password(data.password)
        return crud_user.create(data)

    def verify_password(self, email: str, password: str):
        is_valid = compare_hashed_and_password(
            password, crud_user.get_by_email(email).password
        )
        if not is_valid:
            raise UnauthorizedError()

        return True

    def login(self, email: str, password: str):
        self.verify_password(email, password)

        return LoginTokens(access_token=create_access_token(email))

    def change_pwd(self, current_user: UserRes, change_data: UserPwdChange):
        self.verify_password(current_user.email, change_data.current_password)
        decoded = gen_hashed_password(change_data.change_password)

        crud_user.update(current_user.id, {"password": decoded})
