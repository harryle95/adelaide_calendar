from __future__ import annotations

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.oauth2_token import OAuth2Token  # noqa: TCH001

__all__ = ("User",)


class User(UUIDAuditBase):
    __tablename__ = "user_account_table"
    __table_args__ = {"comment": "User accounts for application access"}
    __pii_columns__ = {"name", "email", "avatar_url"}

    email: Mapped[str | None] = mapped_column(unique=True, index=True, nullable=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=255))
    avatar_url: Mapped[str | None] = mapped_column(String(length=500), nullable=True, default=None)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    oauth2_account: Mapped[OAuth2Token] = relationship(
        back_populates="user",
        lazy="selectin",
        cascade="all, delete",
        uselist=False,
    )
