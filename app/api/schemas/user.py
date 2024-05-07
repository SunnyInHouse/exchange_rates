from pydantic import BaseModel, EmailStr, validator
from pydantic.types import StringConstraints
from typing import Annotated


class UserBase(BaseModel):
    email: Annotated[EmailStr, StringConstraints(max_length=50)]


class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(max_length=100, min_length=3)]

    @validator("email")
    def validate_email(cls, email: EmailStr):
        if email == "admin@admin.ru":
            raise ValueError("BAD email address")
        return email


class UserFromDB(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
