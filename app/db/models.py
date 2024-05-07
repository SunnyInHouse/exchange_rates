from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(length=50), unique=True)
    password: Mapped[str] = mapped_column(String(length=100))
    is_active: Mapped[bool] = mapped_column(default=True, server_default="0")

    def __str__(self) -> str:
        return self.email
