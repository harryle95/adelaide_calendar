import os
from typing import Any

import google_auth_oauthlib.flow
from litestar import Litestar, Request, Response, get
from litestar.datastructures import State
from litestar.response import Redirect

from src.asgi.plugins import alchemy
from src.controller.user.router import UserController
from src.utils.dependencies import create_collection_dependencies
from src.utils.exceptions import exception_to_http_response

__all__ = (
    "authorise",
    "oauth2callback",
)


# --------------------------------------------------------------------------#
# Constants and Environment Variables                                       #
# --------------------------------------------------------------------------#
# This is path to OAuth json creds. Must be a webserver type and not desktop
CLIENT_SECRETS_FILE = ".creds/client_secrets.json"
# Calendar scope - we want to be able to read and write to calendars
SCOPES = ["https://www.googleapis.com/auth/userinfo.profile"]
API_SERVICE_NAME = "calendar"
API_VERSION = "v3"

# By default, OAuth2 requires HTTPS. Setting the follow env var bypasses the
# requirement
# TODO: remove this from production and use TLS
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


@get("/authorise")
async def authorise(state: State) -> Redirect:
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = "http://localhost:8080/oauth2callback"

    authorization_url, authorization_state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )
    state.authorization_state = authorization_state
    return Redirect(authorization_url)


@get("/oauth2callback")
async def oauth2callback(request: Request[Any, Any, Any], state: State) -> Response:
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state.authorization_state,
    )
    flow.redirect_uri = "http://localhost:8080/oauth2callback"

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)
    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session = {"creds": credentials}
    request.set_session(session)
    response = Response(None)
    response.set_cookie("session_auth", credentials.token)
    return response


app = Litestar(
    route_handlers=[UserController, authorise, oauth2callback],
    plugins=[alchemy],
    dependencies=create_collection_dependencies(),
    exception_handlers={
        Exception: exception_to_http_response,
    },
    # on_app_init=[session_auth.on_app_init],
)
