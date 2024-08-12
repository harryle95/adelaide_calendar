"""User Account Controllers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any

from litestar import Controller, Request, delete, get, patch, post
from litestar.di import Provide

from src.controller.user.dependencies import provide_users_service
from src.controller.user.schema import AccountLogin, User, UserCreate, UserUpdate
from src.controller.user.services import UserService
from src.controller.user.urls import AuthURL, UserURL

__all__ = ("UserController",)


if TYPE_CHECKING:
    from uuid import UUID

    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.service import OffsetPagination
    from litestar.params import Dependency, Parameter


class AuthController(Controller):
    """Authentication Controller"""

    tags = ["User Authentication"]
    dependencies = {"users_service": Provide(provide_users_service)}
    signature_namespace = {"UserService": UserService}
    dto = None
    return_dto = None

    @post(
        operation_id="RegisterUser",
        name="auth:register",
        summary="Register User",
        description="Register the user",
        path=AuthURL.REGISTER.value,
        exclude_from_auth=True,
    )
    async def register_user(
        self, users_service: UserService, data: AccountLogin, request: Request[Any, Any, Any]
    ) -> None:
        user = await users_service.create(data)
        request.set_session({"user_id": user.id})
        return

    @post(
        operation_id="LoginUser",
        name="auth:login",
        summary="Login User",
        description="Login the user",
        path=AuthURL.LOGIN.value,
        exclude_from_auth=True,
    )
    async def login_user(
        self,
        users_service: UserService,
        data: AccountLogin,
        request: Request[Any, Any, Any],
    ) -> None:
        user = await users_service.authenticate(data.email, data.password)
        request.set_session({"user_id": user.id})
        return

    @get(
        operation_id="LogoutUser",
        name="auth:logout",
        summary="Logout User",
        description="Logout the user",
        path=AuthURL.LOGOUT.value,
    )
    async def logout_user(
        self,
        request: Request[Any, Any, Any],
    ) -> None:
        request.clear_session()
        return


class UserController(Controller):
    """User Account Controller."""

    tags = ["User Accounts"]
    dependencies = {"users_service": Provide(provide_users_service)}
    signature_namespace = {"UserService": UserService}
    dto = None
    return_dto = None

    @get(
        operation_id="ListUsers",
        name="users:list",
        summary="List Users",
        description="Retrieve the users.",
        path=UserURL.LIST.value,
    )
    async def list_users(
        self,
        users_service: UserService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[User]:
        """List users."""
        results, total = await users_service.list_and_count(*filters)
        return users_service.to_schema(data=results, total=total, schema_type=User, filters=filters)

    @get(
        operation_id="GetUser",
        name="users:get",
        path=UserURL.BY_ID.value,
        summary="Retrieve the details of a user.",
    )
    async def get_user(
        self,
        users_service: UserService,
        user_id: Annotated[
            UUID,
            Parameter(
                title="User ID",
                description="The user to retrieve.",
            ),
        ],
    ) -> User:
        """Get a user."""
        db_obj = await users_service.get(user_id)
        return users_service.to_schema(db_obj, schema_type=User)

    @post(
        operation_id="CreateUser",
        name="users:create",
        summary="Create a new user.",
        cache_control=None,
        description="A user who can login and use the system.",
        path=UserURL.NO_ID.value,
    )
    async def create_user(
        self,
        users_service: UserService,
        data: UserCreate,
    ) -> User:
        """Create a new user."""
        db_obj = await users_service.create(data.to_dict())
        return users_service.to_schema(db_obj, schema_type=User)

    @patch(
        operation_id="UpdateUser",
        name="users:update",
        path=UserURL.BY_ID.value,
    )
    async def update_user(
        self,
        data: UserUpdate,
        users_service: UserService,
        user_id: Annotated[
            UUID,
            Parameter(
                title="User ID",
                description="The user to update.",
            ),
        ],
    ) -> User:
        """Create a new user."""
        db_obj = await users_service.update(item_id=user_id, data=data.to_dict())
        return users_service.to_schema(db_obj, schema_type=User)

    @delete(
        operation_id="DeleteUser",
        name="users:delete",
        path=UserURL.BY_ID.value,
        summary="Remove User",
        description="Removes a user and all associated data from the system.",
    )
    async def delete_user(
        self,
        users_service: UserService,
        user_id: Annotated[
            UUID,
            Parameter(
                title="User ID",
                description="The user to delete.",
            ),
        ],
    ) -> None:
        """Delete a user from the system."""
        _ = await users_service.delete(user_id)
