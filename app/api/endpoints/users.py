from fastapi import APIRouter, Depends

from app.api.schemas.user import UserFromDB
from app.core.dependencies import get_user_repository
from app.core.exceptions import UserNotFound
from app.core.security import get_current_active_user
from app.repositories.user_repository import UserRepository


user_router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(get_current_active_user)]
)


@user_router.get("/", response_model=list[UserFromDB])
async def get_all_users(repo: UserRepository = Depends(get_user_repository)):
    return await repo.get_users()


@user_router.get("/{user_id}/", response_model=UserFromDB)
async def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository),
):
    user = await repo.get_user_by_id(user_id)
    if user is None:
        raise UserNotFound
    return user
