from collections.abc import AsyncGenerator
from typing import Any

from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.controller.user.services import UserService
from src.db.models.user import User

__all__ = ("provide_users_service",)


async def provide_user(request: Request[User, Any, Any]) -> AsyncGenerator[User, None]:
    yield request.user


async def provide_users_service(db_session: AsyncSession) -> AsyncGenerator[UserService, None]:
    """Construct repository and service objects for the request."""
    async with UserService.new(
        session=db_session,
    ) as service:
        yield service
