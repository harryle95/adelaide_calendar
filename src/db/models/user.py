import datetime

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

__all__ = ("User",)


class User(UUIDAuditBase):
    __tablename__ = "user_account"
    __table_args__ = {"comment": "User accounts for application access"}
    __pii_columns__ = {"name", "email", "avatar_url"}

    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    hashed_password: Mapped[str | None] = mapped_column(String(length=255), nullable=True, default=None)
    avatar_url: Mapped[str | None] = mapped_column(String(length=500), nullable=True, default=None)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    joined_at: Mapped[datetime.date] = mapped_column(default=datetime.datetime.now(datetime.UTC))
    last_logged_in_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(datetime.UTC))
