import asyncio
import os
from collections.abc import MutableMapping, Sequence
from datetime import date, datetime, time
from typing import Annotated, Any, cast
from urllib.parse import urlencode

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import requests
from litestar import Litestar, MediaType, Request, get, post
from litestar.connection import ASGIConnection
from litestar.datastructures import State
from litestar.enums import RequestEncodingType
from litestar.exceptions import NotAuthorizedException, ValidationException
from litestar.handlers.base import BaseRouteHandler
from litestar.middleware.session.server_side import (
    ServerSideSessionBackend,
    ServerSideSessionConfig,
)
from litestar.openapi.config import OpenAPIConfig
from litestar.params import Body
from litestar.response import Redirect
from litestar.security.session_auth import SessionAuth
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from tzlocal import get_localzone_name

__all__ = (
    "EventDTO",
    "OAuthToken",
    "User",
    "UserLoginDTO",
    "authorise",
    "create_event",
    "get_secret_data",
    "get_user_info",
    "hash_plain_text_password",
    "index",
    "login",
    "logout",
    "oauth2callback",
    "register",
    "render_calendar",
    "render_event_form",
    "render_login",
    "render_login_form",
    "render_registration",
    "retrieve_user_handler",
    "revoke",
    "validate_password",
    "validated_user_guard",
)


# --------------------------------------------------------------------------#
# Constants and Environment Variables                                       #
# --------------------------------------------------------------------------#
# This is path to OAuth json creds. Must be a webserver type and not desktop
CLIENT_SECRETS_FILE = ".creds/server_secret.json"
# Calendar scope - we want to be able to read and write to calendars
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
API_SERVICE_NAME = "calendar"
API_VERSION = "v3"

# By default, OAuth2 requires HTTPS. Setting the follow env var bypasses the
# requirement
# TODO: remove this from production and use TLS
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# --------------------------------------------------------------------------#
# Cryptography Utility                                                      #
# --------------------------------------------------------------------------#
# Utility methods for hashing and comparing password digest - use passlib library
# https://passlib.readthedocs.io/en/stable/narr/overview.html
password_context = CryptContext(schemes=["argon2"], deprecated="auto")


async def hash_plain_text_password(password: str | bytes) -> str:
    """Hash a plain-text password to be stored in database

    Args:
        password (str | bytes): plain-text password

    Returns:
        str: hashed password

    Note:
        abit hairy here to make it an async runnable.
        If you don't need async, just call password_context.hash(password)
    """
    return await asyncio.get_running_loop().run_in_executor(None, password_context.hash, password)


async def validate_password(plain_text: str | bytes, hashed: str) -> bool:
    """Check whether plain_text password matched hashed password in database

    Args:
        plain_text (str | bytes): plain-text value provided by user, whose hash should match hashed
        hashed (str): hashed password stored in db

    Returns:
        bool: True if correct plain_text is provided
    """
    valid, _ = await asyncio.get_running_loop().run_in_executor(
        None, password_context.verify_and_update, plain_text, hashed
    )
    return bool(valid)


# --------------------------------------------------------------------------#
# Database Schema                                                           #
# --------------------------------------------------------------------------#
# User schema - each instance corresponds to a row in User table in db
# Password stored as hashed version instead of plain text
# email is the primary key of User table
class User(BaseModel):
    email: EmailStr
    hashed_password: str
    is_authorised: bool = False


# OAuthToken schema - each instance corresponds to a row in OAuth table in db
# user_id is the foreign key, linking User and OAuthToken
# fields are obtained from https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html
class OAuthToken(BaseModel):
    user_email: EmailStr
    token: str | None
    refresh_token: str | None
    token_uri: str | None
    client_id: str | None
    client_secret: str | None
    scopes: Sequence[str]


# Login submission form
class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str


UserSignupDTO = UserLoginDTO


# Event submission form data
class EventDTO(BaseModel):
    summary: str
    location: str
    description: str
    timezone: str
    start_date: date
    start_time: time
    end_date: date
    end_time: time

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "location": self.location,
            "description": self.description,
            "start": {
                "dateTime": datetime.combine(self.start_date, self.start_time).strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": self.timezone,
            },
            "end": {
                "dateTime": datetime.combine(self.end_date, self.end_time).strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": self.timezone,
            },
        }


# This mocks interaction with USER and OAuthDB
MOCK_USER_DB: MutableMapping[EmailStr, User] = {}
MOCK_OAUTH_DB: MutableMapping[EmailStr, OAuthToken] = {}


# --------------------------------------------------------------------------#
# Guard                                                                     #
# --------------------------------------------------------------------------#
async def validated_user_guard(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    """This ensure that user must both logged in (session established) and has authorised with Google

    Args:
        connection (ASGIConnection): _description_
        _ (BaseRouteHandler): _description_

    Raises:
        NotAuthorizedException: _description_
    """
    if not connection.user or not connection.user.is_authorised:
        raise NotAuthorizedException("This feature is only available for validated users")


# --------------------------------------------------------------------------#
# Route handler                                                             #
# --------------------------------------------------------------------------#
@get("/", exclude_from_auth=True, media_type=MediaType.HTML)
async def index(request: Request[Any, Any, Any]) -> str:
    """Display Homepage"""
    session = request.session
    user = session.get("user_email", None)
    auth = session.get("creds", None)
    embedded_link = "https://calendar.google.com/calendar/embed?" + urlencode({"src": user})
    template = "<h1>Welcome</h1>"
    auth_status = "Authorised" if auth else "Unauthorised"
    if user:
        template += f"<p>You are logged in as {user} - status: {auth_status}</p>"
        template += '<p><a href="/user">View user details</a> - will return a 401 Unauthorized if the user has not logged in.</p>'
        template += '<p><a href="/authorise">Authorise with google</a> - if you have not done so or if the token was revoked.</p>'
        template += '<p><a href="/creds">View OAuthToken</a> - will return a 401 Unauthorized if the user has not authorised the app with Google</p>'
        template += '<p><a href="/logout">Logout</a> - clear current session information</p>'
        template += '<p><a href="/revoke">Revoke current OAuth Token</a> - token no longer works and you will have to reauthorise.</p>'
        template += "<br>"
        template += "<h1>Calendar</h1>"
        template += '<p><a href="/calendar">Create event</a></p>'
        template += (
            f'<iframe src="{embedded_link}" style="border: 0" width="800" height="600" frameborder="0"></iframe>'
        )
    else:
        template += "<p>You are not logged in!</p>"
        template += '<p>You should <a href="/login">login</a> or <a href="/register">register</a> </p>'
    return template


def render_login_form(header: str, end_point: str) -> str:
    return f"""
    <h1>{header}</h1>
    <form action={end_point} method="post">
        <label for="email">Email:</label><br>
        <input type="text" id="email" name="email"><br>
        <label for="password">Password:</label><br>
        <input type="text" id="password" name="password"><br>
        <button type="submit">Submit</button>
    </form>
    """


def render_event_form() -> str:
    local_tz = get_localzone_name()
    return f"""
    <h1>Create a new event</h1>
    <form action="/calendar" method="post">
        <label for="summary">summary:</label><br>
        <input type="text" id="summary" name="summary"><br>
        <label for="location">location:</label><br>
        <input type="text" id="location" name="location"><br>
        <label for="description">description:</label><br>
        <input type="text" id="description" name="description"><br>
        <label for="timezone">timezone:</label><br>
        <input type="text" id="timezone" name="timezone" value={local_tz}><br>
        <label for="start_date">start_date:</label><br>
        <input type="date" id="start_date" name="start_date"><br>
        <label for="start_time">start_time:</label><br>
        <input type="time" id="start_time" name="start_time"><br>
        <label for="end_date">end_date:</label><br>
        <input type="date" id="end_date" name="end_date"><br>
        <label for="end_time">end_time:</label><br>
        <input type="time" id="end_time" name="end_time"><br>
        <button type="submit">Submit</button>
    </form>
    """


@get("/calendar", guards=[validated_user_guard], media_type=MediaType.HTML)
async def render_calendar() -> str:
    return render_event_form()


@post("/calendar", guards=[validated_user_guard], media_type=MediaType.HTML)
async def create_event(
    data: Annotated[EventDTO, Body(media_type=RequestEncodingType.URL_ENCODED)],
    request: Request[User, MutableMapping[str, Any], Any],
) -> Redirect:
    auth = {k: v for k, v in request.auth["creds"].items() if k != "user_email"}
    credentials = google.oauth2.credentials.Credentials(**auth)  # type: ignore[no-untyped-call]
    service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    service.events().insert(calendarId="primary", body=data.to_dict()).execute()
    return Redirect("/")


@get("/user")
async def get_user_info(request: Request[User, Any, Any]) -> User:
    return request.user


@get("/creds", guards=[validated_user_guard])
async def get_secret_data(request: Request[User, MutableMapping[str, Any], Any]) -> OAuthToken:
    return cast(OAuthToken, request.auth["creds"])


@get("/register", exclude_from_auth=True, media_type=MediaType.HTML)
async def render_registration() -> str:
    return render_login_form("Register", "/register")


@post("/register", exclude_from_auth=True)
async def register(
    data: Annotated[UserSignupDTO, Body(media_type=RequestEncodingType.URL_ENCODED)],
    request: Request[Any, Any, Any],
) -> Redirect:
    if data.email in MOCK_USER_DB:
        raise ValidationException("A user with the same email already exists")
    # Write User instance to database
    hashed_password = await hash_plain_text_password(data.password)
    new_user = User(email=data.email, hashed_password=hashed_password)
    MOCK_USER_DB[new_user.email] = new_user

    # Set session info to contain user_id
    request.set_session({"user_email": new_user.email})
    return Redirect("/")


@get("/login", exclude_from_auth=True, media_type=MediaType.HTML)
async def render_login() -> str:
    return render_login_form("Login", "/login")


@post("/login", exclude_from_auth=True)
async def login(
    data: Annotated[UserLoginDTO, Body(media_type=RequestEncodingType.URL_ENCODED)],
    request: Request[Any, Any, Any],
) -> Redirect:
    if data.email not in MOCK_USER_DB:
        raise NotAuthorizedException("Invalid username or password")
    password_matched = await validate_password(data.password, MOCK_USER_DB[data.email].hashed_password)
    if not password_matched:
        raise NotAuthorizedException("Invalid username or password")

    session: dict[str, Any] = {"user_email": data.email}
    if data.email in MOCK_OAUTH_DB:
        session["creds"] = MOCK_OAUTH_DB[data.email]
    request.set_session(session)
    return Redirect("/")


@get("/logout")
async def logout(request: Request[User, MutableMapping[str, Any], Any]) -> None:
    request.clear_session()


@get("/authorise")
async def authorise(request: Request[User, Any, Any], state: State) -> Redirect:
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

    return Redirect(authorization_url)


@get("/oauth2callback", exclude_from_auth=False)
async def oauth2callback(request: Request[User, Any, Any]) -> Redirect:
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=request.url.query_params["state"]
    )
    flow.redirect_uri = "http://localhost:8080/oauth2callback"

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    oauth_creds = OAuthToken(
        user_email=request.user.email,
        token=credentials.token,
        refresh_token=credentials.refresh_token,
        token_uri=credentials.token_uri,  # type: ignore[reportArgumentType]
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scopes=credentials.scopes,  # type: ignore[reportArgumentType]
    )
    MOCK_OAUTH_DB[request.user.email] = oauth_creds
    MOCK_USER_DB[request.user.email].is_authorised = True
    session = {"user_email": request.user.email, "creds": oauth_creds}
    request.set_session(session)
    return Redirect("/")


@get("/revoke", guards=[validated_user_guard])
async def revoke(request: Request[User, MutableMapping[str, Any], Any]) -> None:
    auth = {k: v for k, v in request.auth["creds"].items() if k != "user_email"}
    credentials = google.oauth2.credentials.Credentials(**auth)  # type: ignore[no-untyped-call]

    revoke = requests.post(  # noqa: S113
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    revoke.raise_for_status()


# We add the session security schema to the OpenAPI config.
openapi_config = OpenAPIConfig(
    title="My API",
    version="1.0.0",
)


async def retrieve_user_handler(
    session: MutableMapping[str, Any], connection: "ASGIConnection[Any, Any, Any, Any]"
) -> User | None:
    return MOCK_USER_DB[session["user_email"]] if session and session.get("user_email") else None


# Session Authentication Middlewarer
session_auth = SessionAuth[User, ServerSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=ServerSideSessionConfig(),
    exclude=["/schema"],
)

app = Litestar(
    route_handlers=[
        index,
        register,
        login,
        logout,
        get_secret_data,
        authorise,
        oauth2callback,
        revoke,
        get_user_info,
        render_login,
        render_registration,
        render_calendar,
        create_event,
    ],
    state=State({}),
    on_app_init=[session_auth.on_app_init],
    openapi_config=openapi_config,
)
