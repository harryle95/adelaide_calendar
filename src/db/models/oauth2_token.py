from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.db.models.user import User


__all__ = ("OAuth2Token",)


class OAuth2Token(UUIDAuditBase):
    __tablename__ = "oauth2_token"
    __table_args__ = {"comment": "User OAuth2 Token"}

    access_token: Mapped[str]
    expires_in: Mapped[int]
    scope: Mapped[str]
    token_type: Mapped[str]
    id_token: Mapped[str]
    expires_at: Mapped[str]

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "user_account.id",
            ondelete="cascade",
        ),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="oauth2_account",
        innerjoin=True,
        lazy="joined",
    )
