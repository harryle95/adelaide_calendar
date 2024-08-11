from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.controller.user.services import UserService


async def provide_users_service(db_session: AsyncSession) -> AsyncGenerator[UserService, None]:
    """Construct repository and service objects for the request."""
    async with UserService.new(
        session=db_session,
    ) as service:
        yield service
