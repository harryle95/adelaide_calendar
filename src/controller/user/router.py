"""User Account Controllers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any, cast

from litestar import Controller, Request, delete, get, patch, post
from litestar.di import Provide
from litestar.exceptions import PermissionDeniedException
from litestar.response import Redirect

from src.controller.user.dependencies import provide_oauth2_token_service, provide_users_service
from src.controller.user.schema import User, UserChangePassword, UserCreate, UserLogin, UserUpdate
from src.controller.user.services import GoogleOAuth2FlowService, OAuth2TokenService, UserService
from src.controller.user.urls import AdminURL, AuthURL, MeURL
from src.db.models.user import User as UserModel  # noqa: TCH001

if TYPE_CHECKING:
    from uuid import UUID

    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.service import OffsetPagination
    from litestar.datastructures import State
    from litestar.params import Dependency, Parameter


__all__ = (
    "AdminController",
    "AuthController",
    "MeController",
)

# TODO: at login, if token expires, refresh token
# TODO: register and login with OIDC, google SDK
# TODO: add revoke method
# TODO: add calendar manipulation APIs
# TODO: use some mail clients to send email for user verification and for resetting password
# TODO: for backend, persistent session with Redis instead of in memory
# TODO: for frontend, persistent login with local/session storage
# TODO: use docker for setting up proper database and cache store servers
# TODO: containerised deployment with Nectr
# TODO: setup SSR with Remix


class AuthController(Controller):
    """Authentication Controller"""

    tags = ["User Authentication"]
    dependencies = {
        "users_service": Provide(provide_users_service),
        "token_service": Provide(provide_oauth2_token_service),
    }
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
    ) -> User:
        """Create a new user.

        Does not require login or superuser privillege. Fails if integrity checks fail - i.e. clashing username
        Returns the user information and automatically login the user if successful.

        Args:
            users_service (UserService): user service layer
            data (UserCreate): user data required to create a new user object
            request (Request[Any, Any, Any]): litestar's Request object to set session

        Returns:
            User: created user data if operation is successful
        """
        user = await users_service.register(data)
        request.set_session({"user_id": user.id})
        return users_service.to_schema(user, schema_type=User)

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
    ) -> User:
        """Authenticate user, and if successful, login the user.

        Does not require login or admin privillege. Fails if user does not exist on the database or the provided password is incorrect.
        Returns user information and login the user if the operation is successful.

        Args:
            users_service (UserService): user service layer
            data (UserLogin): login data
            request (Request[Any, Any, Any]): request object to set session

        Returns:
            User: user information
        """
        user = await users_service.authenticate(data.name_or_email, data.password)
        request.set_session({"user_id": user.id})
        return users_service.to_schema(user, schema_type=User)

    @post(
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
        """Remove user from session

        Requires user to be logged in.

        Args:
            request (Request[Any, Any, Any]): request object to clear session information
        """
        request.clear_session()
        return

    @get(
        operation_id="AuthoriseUser",
        name="auth:authorise",
        summary="Authorise User",
        description="Authorise User",
        path=AuthURL.AUTHORIZE.value,
    )
    async def authorise(self, state: State, request: Request[UserModel, Any, Any]) -> Redirect:
        flow = GoogleOAuth2FlowService.from_client_secrets_file(
            ".creds/google_secrets.json",
            scope=["openid", "email", "profile"],
        )
        redirect_uri = flow.client_config["redirect_uris"]
        flow.redirect_uri = redirect_uri if isinstance(redirect_uri, str) else redirect_uri[0]
        url, flow_state, nonce = flow.authorization_url(access_type="offline")

        # Save nonce and state value for further validation
        state["state"] = flow_state
        state["nonce"] = nonce
        state["user_id"] = request.user.id
        return Redirect(url)

    @get(
        operation_id="OAuth2Callback",
        name="auth:OAuth2Callback",
        summary="Handle Token Fetching",
        description="Token fetching and validation",
        path=AuthURL.OAUTH_REDIRECT.value,
        exclude_from_auth=True,
    )
    async def oauth2callback(
        self,
        request: Request[Any, Any, Any],
        state: State,
        token_service: OAuth2TokenService,
        users_service: UserService,
    ) -> Redirect:
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

        # Add to db
        user_id = state["user_id"]
        user = await users_service.get_one(id=user_id)
        await token_service.add_token(data=credentials, user_id=user_id)
        user.is_verified = True
        await token_service.repository.session.commit()
        await users_service.repository.session.commit()
        request.set_session({"user_id": user_id})
        return Redirect("https://localhost:5173")


class AdminController(Controller):
    """Admin Account Controller."""

    tags = ["Admin Accounts"]
    dependencies = {"users_service": Provide(provide_users_service)}
    signature_namespace = {"UserService": UserService}
    dto = None
    return_dto = None

    @get(
        operation_id="ListUsers",
        name="users:list",
        summary="List Users",
        description="Retrieve the users.",
        path=AdminURL.LIST.value,
    )
    async def list_users(
        self,
        users_service: UserService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[User]:
        """Retrieve all users in the current database. Currently requires login to access this. Will require
        admin privilege in the future

        Args:
            users_service (UserService): user service object
            filters (Annotated[list[FilterTypes], Dependency, optional): filter object based on the data's fields. Defaults to True)].

        Returns:
            OffsetPagination[User]: pagination object
        """
        results, total = await users_service.list_and_count(*filters)
        return users_service.to_schema(data=results, total=total, schema_type=User, filters=filters)

    @get(
        operation_id="GetUser",
        name="users:get",
        path=AdminURL.BY_ID.value,
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
        """Get user based on user id. Currently requires login. Will require admin privilege in the future

        Args:
            users_service (UserService): user service
            user_id (Annotated[ UUID, Parameter, optional): user to search based on id. Defaults to "User ID", description="The user to retrieve.", ), ].

        Returns:
            User: matched user
        """
        db_obj = await users_service.get(user_id)
        return users_service.to_schema(db_obj, schema_type=User)

    @patch(
        operation_id="UpdateUser",
        name="users:update",
        path=AdminURL.BY_ID.value,
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
        """Update user based on user id. Currently requires login. Will require admin privilege in the future.

        This method is used to update username and avatar_url. Updating password has its own method

        Args:
            data (UserUpdate): update information
            users_service (UserService): user service
            user_id (Annotated[ UUID, Parameter, optional): user to search based on id. Defaults to "User ID", description="The user to retrieve.", ), ].

        Returns:
            User: matched user
        """
        db_obj = await users_service.update(item_id=user_id, data=data.to_dict())
        return users_service.to_schema(db_obj, schema_type=User)

    @delete(
        operation_id="DeleteUser",
        name="users:delete",
        path=AdminURL.BY_ID.value,
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
        """Delete a user from database. Currently requires login privilege. Will require admin privilege in the future

        Args:
            users_service (UserService): user service object
            user_id (Annotated[ UUID, Parameter, optional): _description_. Defaults to "User ID", description="The user to delete.", ), ].
        """
        _ = await users_service.delete(user_id)

    @post(
        operation_id="UpdatePassword",
        name="users:updatePassword",
        path=AdminURL.UPDATE_PASSWORD.value,
    )
    async def update_password(
        self,
        data: UserChangePassword,
        users_service: UserService,
        user_id: Annotated[
            UUID,
            Parameter(
                title="User ID",
                description="The user to update.",
            ),
        ],
    ) -> User:
        """Update user based on user id. Currently requires login. Will require admin privilege in the future.

        This method is used to update username and avatar_url. Updating password has its own method

        Args:
            data (UserUpdate): update information
            users_service (UserService): user service
            user_id (Annotated[ UUID, Parameter, optional): user to search based on id. Defaults to "User ID", description="The user to retrieve.", ), ].

        Returns:
            User: matched user
        """
        db_obj = await users_service.update_password(
            user_id=user_id, old_password=data.old_password, new_password=data.new_password
        )
        return users_service.to_schema(db_obj, schema_type=User)


class MeController(Controller):
    """Personal Account Controller."""

    tags = ["Personal Accounts"]
    dependencies = {"users_service": Provide(provide_users_service)}
    signature_namespace = {"UserService": UserService}
    dto = None
    return_dto = None

    @get(
        operation_id="GetMe",
        name="me:get",
        path=MeURL.BASE.value,
        summary="Retrieve the details of the currently logged in user.",
    )
    async def get_my_profile(
        self,
        request: Request[UserModel, Any, Any],
        users_service: UserService,
    ) -> User:
        """Get profile of currently logged in user.

        Args:
            request (Request[UserModel, Any, Any]): request class
            users_service (UserService): user service class

        Returns:
            User: logged in user information
        """
        return users_service.to_schema(request.user, schema_type=User)

    @patch(
        operation_id="UpdateMe",
        name="me:update",
        path=MeURL.BASE.value,
    )
    async def update_me(
        self, data: UserUpdate, users_service: UserService, request: Request[UserModel, Any, Any]
    ) -> User:
        """Update data for the current user.

        Args:
            data (UserUpdate): _description_
            users_service (UserService): _description_
            request (Request[UserModel, Any, Any]): _description_

        Returns:
            User: _description_
        """
        user_id = request.user.id
        db_obj = await users_service.update(item_id=user_id, data=data.to_dict())
        return users_service.to_schema(db_obj, schema_type=User)

    @post(
        operation_id="UpdateMyPassword",
        name="me:updatePassword",
        path=MeURL.UPDATE_PASSWORD.value,
    )
    async def update_my_password(
        self, data: UserChangePassword, users_service: UserService, request: Request[UserModel, Any, Any]
    ) -> User:
        """Update the current user's password

        Args:
            data (UserChangePassword): contains old and new passwords
            users_service (UserService): user service
            request (Request[UserModel, Any, Any]): request object

        Returns:
            User: updated user data
        """
        user_id = request.user.id
        db_obj = await users_service.update_password(
            user_id=user_id, old_password=data.old_password, new_password=data.new_password
        )
        return users_service.to_schema(db_obj, schema_type=User)
