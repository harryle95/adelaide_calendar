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
