from sqlalchemy.exc import IntegrityError
from app.models.base import Base


class NotFoundError(Exception):
    @staticmethod
    def is_not_foreign_key_existed(e: IntegrityError) -> bool:
        code = e.orig.args[0]
        return code == 1216

    @staticmethod
    def validate_exists(model: Base, message="데이터가 존재하지 않습니다") -> None:
        if model is None or model.deleted_at is not None:
            raise NotFoundError(message)
