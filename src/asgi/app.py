from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

import hishel
from authlib.common.security import generate_token
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.jose import jwt
from authlib.oidc.core import CodeIDToken
from litestar import Litestar, Request, get
from litestar.datastructures import State
from litestar.response import Redirect

from src.asgi.plugins import alchemy
from src.controller.proxy.router import ProxyController
from src.controller.user.guards import session_auth
from src.controller.user.router import AuthController, UserController
from src.utils.dependencies import create_collection_dependencies
from src.utils.exceptions import exception_to_http_response


class OAuth2FlowService:
    def __init__(
        self,
        session: AsyncOAuth2Client,
        client_config: Mapping[str, str | Sequence[str]],
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
        cls, client_config: Mapping[str, Any], scope: str | Sequence[str], **kwargs: Any
    ) -> OAuth2FlowService:
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
    ) -> OAuth2FlowService:
        """Creates an instance from a client secrets file.

        Args:
            client_secrets_file (str): The path to the client secrets .json
                file.
            scope (Sequence[str]): The list of scopes to request during the
                flow.
            kwargs: Any additional parameters passed to
                :class:`requests_oauthlib.OAuth2Session`

        Returns:
            Flow: The constructed Flow instance.
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
        :meth:`requests_oauthlib.OAuth2Session.authorization_url`
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


class GoogleOAuth2FlowService(OAuth2FlowService):
    GOOGLE_OAUTH2_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"
    GOOGLE_APIS_CERTS_URL = "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
    GOOGLE_ISSUERS = ["accounts.google.com", "https://accounts.google.com"]

    async def _fetch_certs(self, certs_url: str) -> Mapping[str, str]:
        async with hishel.AsyncCacheClient() as client:
            response = await client.get(certs_url)
        return cast(Mapping[str, str], response.json())

    async def verify_token(self, id_token: str) -> Mapping[str, Any]:
        cert_urls = self.GOOGLE_OAUTH2_CERTS_URL
        certs = await self._fetch_certs(certs_url=cert_urls)
        claims = jwt.decode(id_token, certs, claims_cls=CodeIDToken)
        claims.validate()
        return cast(Mapping[str, Any], claims)


@get("/authorise", exclude_from_auth=True)
async def authorise(state: State) -> Redirect:
    flow = GoogleOAuth2FlowService.from_client_secrets_file(
        ".creds/google_secrets.json", scope=["openid", "email", "profile"]
    )
    flow.redirect_uri = "http://localhost:8080/oauth2callback"
    url, flow_state, nonce = flow.authorization_url(state=state)
    state["state"] = flow_state
    state["nonce"] = nonce
    return Redirect(url)


@get("/oauth2callback", exclude_from_auth=True)
async def oauth2callback(request: Request[Any, Any, Any]) -> None:
    flow = cast(
        GoogleOAuth2FlowService,
        GoogleOAuth2FlowService.from_client_secrets_file(
            ".creds/google_secrets.json", scope=["openid", "email", "profile"]
        ),
    )
    flow.redirect_uri = "http://localhost:8080/oauth2callback"

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = str(request.url)
    credentials = await flow.fetch_token(authorization_response=authorization_response)
    session_data = {"credentials": credentials}
    breakpoint()
    if id_token_raw := credentials.get("id_token"):
        id_decoded = await flow.verify_token(id_token_raw)
        session_data["id_token"] = id_decoded
        print(id_decoded)
    request.set_session(session_data)


app = Litestar(
    route_handlers=[UserController, AuthController, ProxyController, authorise, oauth2callback],
    plugins=[alchemy],
    dependencies=create_collection_dependencies(),
    exception_handlers={
        Exception: exception_to_http_response,
    },
    on_app_init=[session_auth.on_app_init],
)
