from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.db.models.oauth2_token import OAuth2Token
from src.db.models.user import User

__all__ = ("UserRepository", "OAuth2TokenRepository")


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User


class OAuth2TokenRepository(SQLAlchemyAsyncRepository[OAuth2Token]):
    model_type = OAuth2Token
