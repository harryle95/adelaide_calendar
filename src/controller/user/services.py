from typing import Any

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from litestar.exceptions import PermissionDeniedException

from src.controller.user.repositories import UserRepository
from src.db.models.user import User

__all__ = ("UserService",)


class UserService(SQLAlchemyAsyncRepositoryService[User]):
    def __init__(self, **kwargs: Any) -> None:
        self.repository = UserRepository(**kwargs)
        self.model_type = User

    async def authenticate(self, email: str) -> User:
        """Authenticate a user.

        Args:
            email (str): user email

        Raises:
            NotAuthorizedException: Raised when the user doesn't exist

        Returns:
            User: The user object
        """
        db_obj = await self.get_one_or_none(email=email)
        if db_obj is None:
            msg = "User not found or password invalid"
            raise PermissionDeniedException(msg)
        return db_obj
