from typing import Any

from litestar.connection.base import ASGIConnection, AuthT, HandlerT, StateT, UserT
from litestar.exceptions import PermissionDeniedException
from litestar.handlers import BaseRouteHandler
from litestar.middleware.session.server_side import ServerSideSessionBackend, ServerSideSessionConfig
from litestar.security.session_auth import SessionAuth

from src.config.app import alchemy
from src.controller.user.dependencies import provide_users_service
from src.db.models.user import User

__all__ = (
    "require_superuser",
    "retrieve_user_handler",
)


def require_superuser(connection: ASGIConnection[HandlerT, User, AuthT, StateT], _: BaseRouteHandler) -> None:
    if not connection.user or not connection.user.is_superuser:
        raise PermissionDeniedException("Operation requires superuser privilege")


async def retrieve_user_handler(
    session: dict[str, Any], connection: ASGIConnection[HandlerT, UserT, AuthT, StateT]
) -> User | None:
    service = await anext(provide_users_service(alchemy.provide_session(connection.app.state, connection.scope)))
    session_id = session.get("user_id")
    return await service.get_one_or_none(id=session_id)


session_auth = SessionAuth[User, ServerSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=ServerSideSessionConfig(samesite="none", secure=True, httponly=True),
    exclude=["/schema"],
)
