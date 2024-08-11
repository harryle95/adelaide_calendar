from uuid import UUID

import msgspec

from src.utils.schema import CamelizedBaseStruct


class User(CamelizedBaseStruct):
    id: UUID
    email: str
    name: str | None
    is_superuser: bool
    is_verified: bool


class UserCreate(CamelizedBaseStruct):
    email: str
    password: str
    name: str | None = None
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(CamelizedBaseStruct, omit_defaults=True):
    email: str | None | msgspec.UnsetType = msgspec.UNSET
    password: str | None | msgspec.UnsetType = msgspec.UNSET
    name: str | None | msgspec.UnsetType = msgspec.UNSET
    is_superuser: bool | None | msgspec.UnsetType = msgspec.UNSET
    is_verified: bool | None | msgspec.UnsetType = msgspec.UNSET


class AccountLogin(CamelizedBaseStruct):
    username: str
    password: str
