from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated

from app.api.schemas.tokens import TokenData
from app.api.schemas.user import UserCreate
from app.core.config import settings
from app.core.dependencies import get_user_repository
from app.core.exceptions import (
    AccessTokenExpired,
    AccessTokenUncorrect,
    AuthenticationFailed,
    InActiveUser,
    JWTValidateExceptions,
)
from app.db.models import User
from app.repositories.user_repository import UserRepository
from app.utils.password import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/register")


def authenticate_user(user: UserCreate, password: str) -> User:
    if not user or not verify_password(password, user.password):
        return False
    return True


async def create_access_token(data: str, expires_delta: timedelta | None = None):
    to_encode = {"sub": data}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def verify_access_token(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.JWT_ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        expire_in_seconds = payload.get("exp")
        email = payload.get("sub")
    except JWTError:
        raise JWTValidateExceptions

    if (expire_in_seconds is None) or (email is None):
        raise AccessTokenUncorrect

    expire_datetime = datetime.fromtimestamp(expire_in_seconds, tz=timezone.utc)
    if datetime.now(timezone.utc) > expire_datetime:
        raise AccessTokenExpired

    return TokenData(email=email, exp=expire_datetime)


async def get_current_user(
    token: TokenData = Depends(verify_access_token),
    repo: UserRepository = Depends(get_user_repository),
) -> User:
    user = await repo.get_user_by_email(token.email)
    if user is None:
        raise AuthenticationFailed
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise InActiveUser
    return current_user
