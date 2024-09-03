from litestar import Litestar

from src.asgi.plugins import alchemy
from src.config.app import compression, cors, csrf, response_cache
from src.controller.proxy.router import ProxyController
from src.controller.user.guards import session_auth
from src.controller.user.router import AdminController, AuthController, MeController
from src.utils.dependencies import create_collection_dependencies
from src.utils.exceptions import exception_to_http_response

app = Litestar(
    route_handlers=[MeController, AuthController, ProxyController, AdminController],
    plugins=[alchemy],
    dependencies=create_collection_dependencies(),
    exception_handlers={
        Exception: exception_to_http_response,
    },
    on_app_init=[session_auth.on_app_init],
    response_cache_config=response_cache,
    cors_config=cors,
    compression_config=compression,
    csrf_config=csrf,
)
