from advanced_alchemy.extensions.litestar.plugins import SQLAlchemyPlugin

from src.config import alchemy as alchemy_config

alchemy = SQLAlchemyPlugin(config=alchemy_config)
