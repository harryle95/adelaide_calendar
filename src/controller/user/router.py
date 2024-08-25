"""User Account Controllers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any, cast

from litestar import Controller, Request, delete, get, post
from litestar.di import Provide
from litestar.exceptions import PermissionDeniedException
from litestar.response import Redirect

from src.controller.user.dependencies import provide_users_service
from src.controller.user.schema import User, UserCreate, UserLogin
from src.controller.user.services import GoogleOAuth2FlowService, UserService
from src.controller.user.urls import AuthURL, UserURL

__all__ = ("UserController",)


if TYPE_CHECKING:
    from uuid import UUID

    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.service import OffsetPagination
    from litestar.datastructures import State
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
        self, users_service: UserService, data: UserCreate, request: Request[Any, Any, Any]
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
        data: UserLogin,
        request: Request[Any, Any, Any],
    ) -> None:
        user = await users_service.authenticate(data.email)
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

    @get(
        operation_id="AuthoriseUser",
        name="auth:authorise",
        summary="Authorise User",
        description="Authorise User",
        path=AuthURL.AUTHORIZE.value,
        exclude_from_auth=True,
    )
    async def authorise(self, state: State) -> Redirect:
        flow = GoogleOAuth2FlowService.from_client_secrets_file(
            ".creds/google_secrets.json", scope=["openid", "email", "profile"]
        )
        redirect_uri = flow.client_config["redirect_uris"]
        flow.redirect_uri = redirect_uri if isinstance(redirect_uri, str) else redirect_uri[0]
        url, flow_state, nonce = flow.authorization_url()

        # Save nonce and state value for further validation
        state["state"] = flow_state
        state["nonce"] = nonce
        return Redirect(url)

    @get(
        operation_id="OAuth2Callback",
        name="auth:OAuth2Callback",
        summary="Handle Token Fetching",
        description="Token fetching and validation",
        path=AuthURL.OAUTH_REDIRECT.value,
        exclude_from_auth=True,
    )
    async def oauth2callback(self, request: Request[Any, Any, Any], state: State) -> None:
        # Validate state parameter
        param_state = request.query_params["state"]
        if param_state != state["state"]:
            raise PermissionDeniedException("Invalid state parameter")

        # Get token flow
        flow = cast(
            GoogleOAuth2FlowService,
            GoogleOAuth2FlowService.from_client_secrets_file(
                ".creds/google_secrets.json", scope=["openid", "email", "profile"]
            ),
        )
        # TODO: set to current uri
        redirect_uri = flow.client_config["redirect_uris"]
        flow.redirect_uri = redirect_uri if isinstance(redirect_uri, str) else redirect_uri[0]

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = str(request.url)
        credentials = await flow.fetch_token(authorization_response=authorization_response)
        session_data = {"credentials": credentials}

        # Validate id token if present
        if id_token_raw := credentials.get("id_token"):
            id_decoded = await flow.verify_token(id_token_raw)
            session_data["id_token"] = id_decoded
        request.set_session(session_data)


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
