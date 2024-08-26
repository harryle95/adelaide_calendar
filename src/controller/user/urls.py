from enum import Enum

__all__ = (
    "AdminURL",
    "AuthURL",
    "MeURL",
)


class AuthURL(Enum):
    REGISTER = "/auth/register"
    LOGIN = "/auth/login"
    LOGOUT = "/auth/logout"
    AUTHORIZE = "/auth/authorize"
    OAUTH_REDIRECT = "/auth/oauth2callback"
    REVOKE = "/auth/revoke"


class AdminURL(Enum):
    LIST = "/admin/users"
    NO_ID = "/admin/user"
    BY_ID = "/admin/user/{user_id:uuid}"
    UPDATE_PASSWORD = "/admin/user/password"  # noqa: S105


class MeURL(Enum):
    BASE = "/me"
    UPDATE_PASSWORD = "/me/password"  # noqa: S105
