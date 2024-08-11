from typing import Any

from advanced_alchemy.service import ModelDictT, SQLAlchemyAsyncRepositoryService
from litestar.exceptions import PermissionDeniedException

from src.controller.user.repositories import UserRepository
from src.db.models.user import User
from src.utils.crypt import hash_plain_text_password, validate_password

__all__ = ("UserService", )


class UserService(SQLAlchemyAsyncRepositoryService[User]):
    def __init__(self, **kwargs: Any) -> None:
        self.repository = UserRepository(**kwargs)
        self.model_type = User

    async def to_model(self, data: ModelDictT[User], operation: str | None = None) -> User:
        if isinstance(data, dict) and "password" in data:
            password: bytes | str | None = data.pop("password", None)
            if password is not None:
                data.update({"hashed_password": await hash_plain_text_password(password)})
        return await super().to_model(data, operation)

    async def authenticate(self, username: str, password: bytes | str) -> User:
        """Authenticate a user.

        Args:
            username (str): _description_
            password (str | bytes): _description_

        Raises:
            NotAuthorizedException: Raised when the user doesn't exist, isn't verified, or is not active.

        Returns:
            User: The user object
        """
        db_obj = await self.get_one_or_none(email=username)
        if db_obj is None:
            msg = "User not found or password invalid"
            raise PermissionDeniedException(msg)
        if db_obj.hashed_password is None:
            msg = "User not found or password invalid."
            raise PermissionDeniedException(msg)
        if not await validate_password(password, db_obj.hashed_password):
            msg = "User not found or password invalid"
            raise PermissionDeniedException(msg)
        return db_obj
