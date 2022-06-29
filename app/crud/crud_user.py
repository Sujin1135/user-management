import logging

from sqlalchemy.exc import IntegrityError

from app.core.db import get_db_session
from app.crud.crud_base import CRUDBase
from app.exceptions.not_found_error import NotFoundError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, email: str):
        try:
            session = get_db_session()
            target = session.query(self.model).filter(self.model.email == email).first()

            NotFoundError.validate_exists(target)

            return target
        except IntegrityError as e:
            logging.error("*** occurred a mysql error when get a model by email")
            raise e
        finally:
            session.close()


crud_user = CRUDUser(User)
