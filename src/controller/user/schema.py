from typing import NotRequired, Required, TypedDict
from uuid import UUID

import msgspec

from src.utils.schema import CamelizedBaseStruct

__all__ = (
    "OAuth2Config",
    "User",
    "UserChangePassword",
    "UserCreate",
    "UserLogin",
    "UserResetPasswordComplete",
    "UserResetPasswordInitiate",
    "UserUpdate",
)


class User(CamelizedBaseStruct):
    id: UUID | None
    email: str | None
    name: str | None
    is_superuser: bool
    is_verified: bool
    avatar_url: str | None


class UserLogin(CamelizedBaseStruct):
    name_or_email: str
    password: str


class UserCreate(CamelizedBaseStruct):
    name: str
    email: str
    password: str


class UserChangePassword(CamelizedBaseStruct):
    old_password: str
    new_password: str


class UserResetPasswordInitiate(CamelizedBaseStruct):
    email: str


class UserResetPasswordComplete(CamelizedBaseStruct):
    password: str


class UserUpdate(CamelizedBaseStruct, omit_defaults=True):
    email: str | None | msgspec.UnsetType = msgspec.UNSET
    name: str | None | msgspec.UnsetType = msgspec.UNSET
    avatar_url: str | None | msgspec.UnsetType = msgspec.UNSET


class OAuth2Config(TypedDict):
    client_id: Required[str]
    project_id: NotRequired[str]
    auth_uri: Required[str]
    token_uri: Required[str]
    cert_url: NotRequired[str]
    client_secret: Required[str]
    redirect_uris: Required[str]
