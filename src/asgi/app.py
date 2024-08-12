from litestar import Litestar

from src.asgi.plugins import alchemy
from src.controller.user.guards import session_auth
from src.controller.user.router import UserController
from src.utils.dependencies import create_collection_dependencies
from src.utils.exceptions import exception_to_http_response

app = Litestar(
    route_handlers=[UserController],
    plugins=[alchemy],
    dependencies=create_collection_dependencies(),
    exception_handlers={
        Exception: exception_to_http_response,
    },
    on_app_init=[session_auth.on_app_init],
)
