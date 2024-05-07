from abc import ABC, abstractmethod
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserCreate
from app.core.exceptions import UserAlreadyExists
from app.db.models import User
from app.utils.password import get_password_hash


class UserRepository(ABC):
    @abstractmethod
    async def get_users(self) -> list[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, user_email: EmailStr) -> User:
        pass

    @abstractmethod
    async def create_user(self, user: UserCreate) -> User:
        pass


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self) -> list[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.session.execute(select(User).where(User.id == user_id))
        return user.scalar()

    async def get_user_by_email(self, user_email: EmailStr) -> User:
        user = await self.session.execute(select(User).where(User.email == user_email))
        return user.scalar()

    async def create_user(self, user: UserCreate) -> User:
        if await self.get_user_by_email(user_email=user.email) is not None:
            raise UserAlreadyExists
        new_user = User(email=user.email, password=get_password_hash(user.password))
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
