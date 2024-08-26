from enum import Enum

__all__ = (
    "AuthURL",
    "UserURL",
)


class AuthURL(Enum):
    REGISTER = "/auth/register"
    LOGIN = "/auth/login"
    LOGOUT = "/auth/logout"
    AUTHORIZE = "/auth/authorize"
    OAUTH_REDIRECT = "/auth/oauth2callback"
    REVOKE = "/auth/revoke"


class UserURL(Enum):
    LIST = "/users"
    ME = "/user/me"
    NO_ID = "/user"
    BY_ID = "/user/{user_id:uuid}"
    UPDATE_PASSWORD = "/user/password"  # noqa: S105
