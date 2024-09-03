from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.db.models.user import User

__all__ = ("OAuth2Token",)


class OAuth2Token(UUIDAuditBase):
    __tablename__ = "oauth2_token_table"
    __table_args__ = {"comment": "User OAuth2 Token"}

    access_token: Mapped[str]
    expires_in: Mapped[int]
    refresh_token: Mapped[str]
    scope: Mapped[str]
    token_type: Mapped[str]
    id_token: Mapped[str]
    expires_at: Mapped[str]

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "user_account_table.id",
            ondelete="cascade",
        ),
        nullable=False,
    )

    user: Mapped[User] = relationship(
        back_populates="oauth2_account",
        viewonly=True,
        innerjoin=True,
        lazy="joined",
    )
