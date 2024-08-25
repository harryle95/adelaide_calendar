import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

import httpx
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from authlib.common.security import generate_token
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.jose import jwt
from litestar.exceptions import PermissionDeniedException

from src.controller.user.repositories import UserRepository
from src.controller.user.schema import OAuth2Config
from src.db.models.user import User

__all__ = ("UserService",)


class UserService(SQLAlchemyAsyncRepositoryService[User]):
    def __init__(self, **kwargs: Any) -> None:
        self.repository = UserRepository(**kwargs)
        self.model_type = User

    async def authenticate(self, email: str) -> User:
        """Authenticate a user.

        Args:
            email (str): user email

        Raises:
            NotAuthorizedException: Raised when the user doesn't exist

        Returns:
            User: The user object
        """
        db_obj = await self.get_one_or_none(email=email)
        if db_obj is None:
            msg = "User not found or password invalid"
            raise PermissionDeniedException(msg)
        return db_obj


class OAuth2FlowService:
    """Identity Provider Agnostic OAuth2 Flow service. Performs code flow - in constrast to implicit/hybrid flow"""

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
        self.session = session
        self.client_config = client_config
        self.redirect_uri = redirect_uri
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
        self._credentials = cast(
            Mapping[str, str], await self.session.fetch_token(url=self.client_config["token_uri"], **kwargs)
        )
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
