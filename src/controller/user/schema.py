from typing import NotRequired, Required, TypedDict
from uuid import UUID

from src.utils.schema import CamelizedBaseStruct

__all__ = (
    "OAuth2Config",
    "User",
    "UserChangePassword",
    "UserCreate",
    "UserLogin",
    "UserResetPasswordComplete",
    "UserResetPasswordInitiate",
)


class User(CamelizedBaseStruct):
    id: UUID
    email: str | None
    name: str
    is_superuser: bool
    is_verified: bool


class UserLogin(CamelizedBaseStruct):
    name_or_email: str
    password: str


class UserCreate(CamelizedBaseStruct):
    name: str
    password: str


class UserChangePassword(CamelizedBaseStruct):
    old_password: str
    new_password: str


class UserResetPasswordInitiate(CamelizedBaseStruct):
    email: str


class UserResetPasswordComplete(CamelizedBaseStruct):
    password: str


class OAuth2Config(TypedDict):
    client_id: Required[str]
    project_id: NotRequired[str]
    auth_uri: Required[str]
    token_uri: Required[str]
    cert_url: NotRequired[str]
    client_secret: Required[str]
    redirect_uris: Required[str]
