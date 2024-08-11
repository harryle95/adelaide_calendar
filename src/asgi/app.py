from litestar import Litestar

from src.asgi.plugins import alchemy
from src.controller.user.router import UserController
from src.utils.dependencies import create_collection_dependencies

app = Litestar(
    route_handlers=[UserController],
    plugins=[alchemy],
    dependencies=create_collection_dependencies(),
)
