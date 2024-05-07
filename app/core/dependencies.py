from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import async_session_maker
from app.repositories.user_repository import UserRepository, SQLAlchemyUserRepository


async def get_async_session():
    async with async_session_maker() as session:
        yield session


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepository:
    return SQLAlchemyUserRepository(session)
