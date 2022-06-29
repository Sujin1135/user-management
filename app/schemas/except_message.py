from pydantic import BaseModel


class ExceptMessage(BaseModel):
    message: str
