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
    id: UUID
    email: str
    name: str
    is_superuser: bool
    is_verified: bool
    avatar_url: str


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


class OAuth2Token(TypedDict):
    access_token: str
    expires_in: int
    scope: str
    token_type: str
    id_token: str
    expires_at: str


class OIDCClaim(TypedDict):
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: str
    at_hash: str
    nonce: str
    name: str
    picture: str
    given_name: str
    family_name: str
    iat: int
    exp: int
