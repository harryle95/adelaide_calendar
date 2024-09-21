import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast
from urllib.parse import quote_plus
from uuid import UUID

import httpx
from advanced_alchemy.service import ModelDictT, SQLAlchemyAsyncRepositoryService
from authlib.common.security import generate_token
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.jose import jwt
from litestar.exceptions import PermissionDeniedException

from src.controller.user.repositories import OAuth2TokenRepository, UserRepository
from src.controller.user.schema import OAuth2Config, UserCreate
from src.db.models.oauth2_token import OAuth2Token
from src.db.models.user import User
from src.utils.crypt import hash_plain_text_password, validate_password

__all__ = ("UserService",)


class UserService(SQLAlchemyAsyncRepositoryService[User]):
    def __init__(self, **kwargs: Any) -> None:
        self.repository = UserRepository(**kwargs)
        self.model_type = User

    async def to_model(self, data: ModelDictT[User], operation: str | None = None) -> User:
        """Utility method to convert between dto and model (sqlalchemy object). The counterpart is
        to_schema

        Convert `password` to `hashed_password` then return the object

        Args:
            data (ModelDictT[User]): dto data - must be converted to a dict.
            operation (str | None, optional): Defaults to None.

        Returns:
            User: sqlalchemy User object
        """
        if isinstance(data, dict):
            encoded_name = quote_plus(data["name"])
            data["avatar_url"] = f"https://ui-avatars.com/api/?name={encoded_name}"
            if "password" in data:
                password: bytes | str | None = data.pop("password", None)
                if password is not None:
                    data.update({"hashed_password": await hash_plain_text_password(password)})

        return await super().to_model(data, operation)

    async def authenticate(self, username: str, password: bytes | str) -> User:
        """Authenticate a user.

        Try to retrieve a user based on either username or email. If the
        user exists, check if password matches.

        Args:
            username (str): username or email
            password (str | bytes): _description_

        Raises:
            NotAuthorizedException: Raised when the user doesn't exist, isn't verified, or is not active.

        Returns:
            User: The user object
        """
        db_obj = await self.get_one_or_none(email=username)
        # Try to get an object by email then username
        if db_obj is None:
            db_obj = await self.get_one_or_none(name=username)
        if db_obj is None:
            raise PermissionDeniedException("User not found or password invalid")
        if db_obj.hashed_password is None:
            raise PermissionDeniedException("User not found or password invalid.")
        if not await validate_password(password, db_obj.hashed_password):
            raise PermissionDeniedException("User not found or password invalid")
        return db_obj

    async def update_password(self, user_id: UUID, old_password: str | None, new_password: str) -> User:
        """Update user password.

        If provided `old_password` matches the previous password, will update user info using
        the new password. If `old_password` is not provided, will simply update user info.

        `old_password` must be provided in the standard update password flow - i.e. updating password from inside a browser.
        `old_password` does not need to be provided when the update password flow is based on a trusted flow. - i.e. updating
        from an updating url sent from the server to the user's authenticated email.

        Args:
            user_id (UUID): user id to retrieve user
            old_password (str | None): previous password provided by user
            new_password (str): new password provided by user

        Raises:
            PermissionDeniedException: if no user matches user_id. Can happen if the user has been deleted
            PermissionDeniedException: if the provided `old_password` does not match the previous password.

        Returns:
            User: user with updated password
        """
        user_obj = await self.get_one_or_none(id=user_id)
        # For preventing race condition
        if not user_obj:
            raise PermissionDeniedException("User does not exist")
        if old_password:
            matched = await validate_password(old_password, user_obj.hashed_password)
            if not matched:
                raise PermissionDeniedException("Old password does not match")
        new_hashed_password = await hash_plain_text_password(new_password)
        user_obj.hashed_password = new_hashed_password
        return user_obj

    async def register(self, data: UserCreate) -> User:
        user_model = await self.to_model(data.to_dict())
        return await self.create(user_model, error_messages={"foreign_key": "Username or email already exists"})


class OAuth2TokenService(SQLAlchemyAsyncRepositoryService[OAuth2Token]):
    def __init__(self, **kwargs: Any) -> None:
        self.repository = OAuth2TokenRepository(**kwargs)
        self.model_type = OAuth2Token

    async def add_token(self, data: Mapping[str, str], user_id: UUID) -> OAuth2Token:
        token_model = await self.to_model(cast(dict, data))
        token_model.user_id = user_id
        return await self.create(token_model)


class OAuth2FlowService:
    """Identity Provider Agnostic OAuth2 Flow service. Performs code flow - in contrast to implicit/hybrid flow"""

    OAUTH2_CERT_URL: str  # URL to public key for jwt decode
    OAUTH2_ISSUERS: str | Sequence[str]  # Identity of Issuer for jwt validation

    def __init__(
        self,
        session: AsyncOAuth2Client,
        client_config: OAuth2Config,
        redirect_uri: str | None = None,
        code_verifier: str | None = None,
        autogenerate_code_verifier: bool = True,
    ) -> None:
        if redirect_uri:
            session.redirect_uri = redirect_uri
        self.session = session
        self.client_config = client_config
        self.code_verifier = code_verifier
        self.autogenerate_code_verifier = autogenerate_code_verifier
        self._credentials: Mapping[str, str] | None = None
        self._token: str | None = None
        self._refresh_token: str | None = None

    @property
    def credentials(self) -> Mapping[str, str] | None:
        return self._credentials

    @property
    def token(self) -> str | None:
        if self._token:
            return self._token
        if self.credentials:
            return self.credentials.get("token")
        return None

    @property
    def refresh_token(self) -> str | None:
        if self.refresh_token:
            return self.refresh_token
        if self.credentials:
            return self.credentials.get("refresh_token")
        return None

    @classmethod
    def from_client_config(
        cls, client_config: OAuth2Config, scope: str | Sequence[str], **kwargs: Any
    ) -> "OAuth2FlowService":
        """Class method to create an instance from client config

        Args:
            client_config (OAuth2Config): dictionary with client information to create a session to authentication and authorisation servers
            scope (str | Sequence[str]): access scope
            kwargs (Any): other parameters - for compatibility with Authlib library

        """
        client = AsyncOAuth2Client(scope=scope, **client_config, **kwargs)
        return cls(
            session=client,
            client_config=client_config,
            redirect_uri=kwargs.get("redirect_uri"),
            code_verifier=kwargs.get("code_verifier"),
            autogenerate_code_verifier=kwargs.get("autogenerate_code_verifier", True),
        )

    @classmethod
    def from_client_secrets_file(
        cls, client_secrets_file: str, scope: str | Sequence[str], **kwargs: Any
    ) -> "OAuth2FlowService":
        """Class method to create an instance from secret file location

        Args:
            client_secrets_file (str): local path to client secrets file
            scope (str | Sequence[str]): access scope
            kwargs (Any): other parameters for compatibility

        Returns:
            OAuth2FlowService: constructed object
        """
        with Path(client_secrets_file).open("r") as json_file:
            client_config = json.load(json_file)["web"]
        return cls.from_client_config(client_config, scope=scope, **kwargs)

    @property
    def redirect_uri(self) -> str | None:
        return cast(str | None, self.session.redirect_uri)

    @redirect_uri.setter
    def redirect_uri(self, value: str) -> None:
        self.session.redirect_uri = value

    def authorization_url(self, **kwargs: Any) -> tuple[str, str, str]:
        """Generates an authorization URL.

        This is the first step in the OAuth 2.0 Authorization Flow. The user's
        browser should be redirected to the returned URL.

        This method calls
        :meth:`authlib.integrations.OAuth2Session.create_authorization_url`
        and specifies the client configuration's authorization URI (usually
        Google's authorization server) and specifies that "offline" access is
        desired. This is required in order to obtain a refresh token.

        Args:
            kwargs: Additional arguments passed through to
                :meth:`requests_oauthlib.OAuth2Session.authorization_url`

        Returns:
            Tuple[str, str, str]: The generated authorization URL, state, and nonce. The
                user must visit the URL to complete the flow. The state is used
                when completing the flow to verify that the request originated
                from your application. If your application is using a different
                :class:`Flow` instance to obtain the token, you will need to
                specify the ``state`` when constructing the :class:`Flow`.
        """
        if self.autogenerate_code_verifier:
            self.code_verifier = generate_token(48)
        self.nonce = generate_token()
        url, state = self.session.create_authorization_url(
            self.client_config["auth_uri"],
            code_verifier=self.code_verifier,
            nonce=self.nonce,
            **kwargs,
        )
        return url, state, self.nonce

    async def fetch_token(self, **kwargs: Any) -> Mapping[str, str]:
        """Completes the Authorization Flow and obtains an access token.

        This is the final step in the OAuth 2.0 Authorization Flow. This is
        called after the user consents.

        This method calls
        :meth:`requests_oauthlib.OAuth2Session.fetch_token`
        and specifies the client configuration's token URI (usually Google's
        token server).

        Args:
            kwargs: Arguments passed through to
                :meth:`requests_oauthlib.OAuth2Session.fetch_token`. At least
                one of ``code`` or ``authorization_response`` must be
                specified.

        Returns:
            Mapping[str, str]: The obtained tokens. Typically, you will not use
                return value of this function and instead use
                :meth:`credentials` to obtain a
                :class:`~google.auth.credentials.Credentials` instance.
        """
        credentials = await self.session.fetch_token(url=self.client_config["token_uri"], **kwargs)  # pyright: ignore
        self._credentials = cast(Mapping[str, str], credentials)
        return self._credentials

    async def _fetch_certs(self, certs_url: str) -> Mapping[str, str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(certs_url)
        return cast(Mapping[str, str], response.json())

    async def verify_token(self, id_token: str) -> Mapping[str, Any]:
        """WIP - will need to check iss, claim and other information"""
        cert_urls = self.client_config.get("cert_url") if self.client_config.get("cert_url") else self.OAUTH2_CERT_URL
        if not cert_urls:
            raise ValueError("Public key url must be provided to decode jwt")
        certs = await self._fetch_certs(certs_url=cert_urls)
        claims = jwt.decode(id_token, certs)
        return cast(Mapping[str, Any], claims)


class GoogleOAuth2FlowService(OAuth2FlowService):
    OAUTH2_CERT_URL = "https://www.googleapis.com/oauth2/v3/certs"
    OAUTH2_ISSUERS = ["accounts.google.com", "https://accounts.google.com"]
