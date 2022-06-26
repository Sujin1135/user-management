from pydantic import BaseModel


class Healthcheck(BaseModel):

    is_ok: bool = True
