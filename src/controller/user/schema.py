from typing import NotRequired, Required, TypedDict
from uuid import UUID

from src.utils.schema import CamelizedBaseStruct

__all__ = ("User", "UserCreate", "UserLogin")


class UserCreate(CamelizedBaseStruct):
    email: str
    name: str | None
    avatar_url: str | None


class User(UserCreate):
    id: UUID
    is_superuser: bool


UserLogin = UserCreate


class OAuth2Config(TypedDict):
    client_id: Required[str]
    project_id: NotRequired[str]
    auth_uri: Required[str]
    token_uri: Required[str]
    cert_url: NotRequired[str]
    client_secret: Required[str]
    redirect_uris: Required[str]
