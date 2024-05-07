from fastapi import APIRouter, Depends

from app.api.schemas.tokens import AccessToken
from app.api.schemas.user import UserCreate, UserFromDB
from app.core.dependencies import get_user_repository
from app.core.exceptions import IncorrectUser
from app.core.security import  authenticate_user, create_access_token
from app.repositories.user_repository import UserRepository


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserFromDB)
async def create_user(
    user: UserCreate, repo: UserRepository = Depends(get_user_repository)
):
    return await repo.create_user(user)


@auth_router.post("/login", response_model=AccessToken)
async def login(
    user_data: UserCreate,
    repo: UserRepository = Depends(get_user_repository),
) -> AccessToken:
    user = await repo.get_user_by_email(user_email=user_data.email)
    print(user)
    if not authenticate_user(user, user_data.password):
        raise IncorrectUser
    access_token = await create_access_token(user.email)
    return AccessToken(access_token=access_token)
