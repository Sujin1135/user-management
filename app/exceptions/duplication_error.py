from sqlalchemy.exc import IntegrityError


class DuplicationError(Exception):
    @staticmethod
    def is_duplication_err(e: IntegrityError):
        code = e.orig.args[0]
        return code == 1062
