from pydantic import BaseModel


class LoginTokens(BaseModel):
    access_token: str
