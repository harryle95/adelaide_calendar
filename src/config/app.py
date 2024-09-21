from typing import cast

from advanced_alchemy.extensions.litestar import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    async_autocommit_before_send_handler,
)
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.config.response_cache import ResponseCacheConfig

from src.config.base import Settings

settings = Settings()

compression = CompressionConfig(backend="gzip")

csrf = CSRFConfig(
    secret=settings.app.SECRET_KEY,
    cookie_name=settings.app.CSRF_COOKIE_NAME,
    cookie_secure=settings.app.CSRF_COOKIE_SECURE,
)
cors = CORSConfig(
    allow_origins=cast(list[str], settings.app.ALLOWED_CORS_ORIGINS),
    allow_credentials=True,
)
alchemy = SQLAlchemyAsyncConfig(
    engine_instance=settings.db.engine,
    create_all=True,
    before_send_handler=async_autocommit_before_send_handler,
    session_config=AsyncSessionConfig(expire_on_commit=False),
)

response_cache = ResponseCacheConfig(default_expiration=120)
