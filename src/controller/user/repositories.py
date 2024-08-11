from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.db.models.user import User

__all__ = ("UserRepository", )


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User
