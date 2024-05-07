from datetime import datetime
from pydantic import BaseModel


class BaseToken(BaseModel):
    token_type: str = "bearer"


class AccessToken(BaseToken):
    access_token: str


class TokenData(BaseModel):
    email: str | None = None
    exp: datetime | None = None
