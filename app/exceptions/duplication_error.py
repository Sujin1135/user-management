from sqlalchemy.exc import IntegrityError

DUPLICATION_CODE = "gkpj"


class DuplicationError(Exception):
    @staticmethod
    def is_duplication_err(e: IntegrityError):
        return e.code == DUPLICATION_CODE
