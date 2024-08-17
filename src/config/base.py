from __future__ import annotations

import binascii
import json
import os
from dataclasses import dataclass, field
from typing import Any

from advanced_alchemy.utils.text import slugify
from litestar.serialization import decode_json, encode_json
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

__all__ = (
    "AppSettings",
    "DatabaseSettings",
    "Settings",
)


DEFAULT_MODULE_NAME = "app"

TRUE_VALUES = {"True", "true", "1", "yes", "Y", "T"}


@dataclass
class DatabaseSettings:
    """Contains connection engine settings for sqlalchemy. See more:
    https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine
    """

    ECHO: bool = field(
        default_factory=lambda: os.getenv("DATABASE_ECHO", "False") in TRUE_VALUES,
    )
    """Enable SQLAlchemy engine logs."""
    ECHO_POOL: bool = field(
        default_factory=lambda: os.getenv("DATABASE_ECHO_POOL", "False") in TRUE_VALUES,
    )
    """Enable SQLAlchemy connection pool logs."""
    POOL_DISABLED: bool = field(
        default_factory=lambda: os.getenv("DATABASE_POOL_DISABLED", "False") in TRUE_VALUES,
    )
    """Disable SQLAlchemy pool configuration."""
    POOL_MAX_OVERFLOW: int = field(default_factory=lambda: int(os.getenv("DATABASE_MAX_POOL_OVERFLOW", "10")))
    """Max overflow for SQLAlchemy connection pool"""
    POOL_SIZE: int = field(default_factory=lambda: int(os.getenv("DATABASE_POOL_SIZE", "5")))
    """Pool size for SQLAlchemy connection pool"""
    POOL_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("DATABASE_POOL_TIMEOUT", "30")))
    """Time in seconds for timing connections out of the connection pool."""
    POOL_RECYCLE: int = field(default_factory=lambda: int(os.getenv("DATABASE_POOL_RECYCLE", "300")))
    """Amount of time to wait before recycling connections."""
    POOL_PRE_PING: bool = field(
        default_factory=lambda: os.getenv("DATABASE_PRE_POOL_PING", "False") in TRUE_VALUES,
    )
    """Optionally ping database before fetching a session from the connection pool."""
    URL: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3"))
    _engine_instance: AsyncEngine | None = None
    """SQLAlchemy engine instance generated from settings."""

    @property
    def engine(self) -> AsyncEngine:
        return self.get_engine()

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance is not None:
            return self._engine_instance
        if self.URL.startswith("postgresql+asyncpg"):
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
                pool_use_lifo=True,  # use lifo to reduce the number of idle connections
                poolclass=NullPool if self.POOL_DISABLED else None,
            )
            """Database session factory.

            See [`async_sessionmaker()`][sqlalchemy.ext.asyncio.async_sessionmaker].
            """

            @event.listens_for(engine.sync_engine, "connect")
            def _sqla_on_connect(dbapi_connection: Any, _: Any) -> Any:  # pragma: no cover
                """Using msgspec for serialization of the json column values means that the
                output is binary, not `str` like `json.dumps` would output.
                SQLAlchemy expects that the json serializer returns `str` and calls `.encode()` on the value to
                turn it to bytes before writing to the JSONB column. I'd need to either wrap `serialization.to_json` to
                return a `str` so that SQLAlchemy could then convert it to binary, or do the following, which
                changes the behaviour of the dialect to expect a binary value from the serializer.
                See Also https://github.com/sqlalchemy/sqlalchemy/blob/14bfbadfdf9260a1c40f63b31641b27fe9de12a0/lib/sqlalchemy/dialects/postgresql/asyncpg.py#L934  pylint: disable=line-too-long
                """

                def encoder(bin_value: bytes) -> bytes:
                    return b"\x01" + encode_json(bin_value)

                def decoder(bin_value: bytes) -> Any:
                    # the byte is the \x01 prefix for jsonb used by PostgreSQL.
                    # asyncpg returns it when format='binary'
                    return decode_json(bin_value[1:])

                dbapi_connection.await_(
                    dbapi_connection.driver_connection.set_type_codec(
                        "jsonb",
                        encoder=encoder,
                        decoder=decoder,
                        schema="pg_catalog",
                        format="binary",
                    ),
                )
                dbapi_connection.await_(
                    dbapi_connection.driver_connection.set_type_codec(
                        "json",
                        encoder=encoder,
                        decoder=decoder,
                        schema="pg_catalog",
                        format="binary",
                    ),
                )
        elif self.URL.startswith("sqlite+aiosqlite"):
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
            )
            """Database session factory.

            See [`async_sessionmaker()`][sqlalchemy.ext.asyncio.async_sessionmaker].
            """

            @event.listens_for(engine.sync_engine, "connect")
            def _sqla_on_connect(dbapi_connection: Any, _: Any) -> Any:  # pragma: no cover
                """Override the default begin statement.  The disables the built in begin execution."""
                dbapi_connection.isolation_level = None

            @event.listens_for(engine.sync_engine, "connect")
            def _enable_foreign_key(dbapi_connection, connection_record):  # type: ignore[no-untyped-def]
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

            @event.listens_for(engine.sync_engine, "begin")
            def _sqla_on_begin(dbapi_connection: Any) -> Any:  # pragma: no cover
                """Emits a custom begin"""
                dbapi_connection.exec_driver_sql("BEGIN")

        else:
            engine = create_async_engine(
                url=self.URL,
                future=True,
                json_serializer=encode_json,
                json_deserializer=decode_json,
                echo=self.ECHO,
                echo_pool=self.ECHO_POOL,
                max_overflow=self.POOL_MAX_OVERFLOW,
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_recycle=self.POOL_RECYCLE,
                pool_pre_ping=self.POOL_PRE_PING,
            )
        self._engine_instance = engine
        return self._engine_instance


@dataclass
class AppSettings:
    """Application configuration"""

    URL: str = field(default_factory=lambda: os.getenv("APP_URL", "http://localhost:8000"))
    """The frontend base URL"""
    DEBUG: bool = field(default_factory=lambda: os.getenv("LITESTAR_DEBUG", "False") in TRUE_VALUES)
    """Run `Litestar` with `debug=True`."""
    SECRET_KEY: str = field(
        default_factory=lambda: os.getenv("SECRET_KEY", binascii.hexlify(os.urandom(32)).decode(encoding="utf-8")),
    )
    """Application secret key."""
    NAME: str = field(default_factory=lambda: "app")
    """Application name."""
    ALLOWED_CORS_ORIGINS: list[str] | str = field(default_factory=lambda: os.getenv("ALLOWED_CORS_ORIGINS", '["*"]'))
    """Allowed CORS Origins"""
    CSRF_COOKIE_NAME: str = field(default_factory=lambda: "csrftoken")
    """CSRF Cookie Name"""
    CSRF_COOKIE_SECURE: bool = field(default_factory=lambda: False)
    """CSRF Secure Cookie"""
    JWT_ENCRYPTION_ALGORITHM: str = field(default_factory=lambda: "HS256")
    """JWT Encryption Algorithm"""

    @property
    def slug(self) -> str:
        """Return a slugified name.

        Returns:
            `self.NAME`, all lowercase and hyphens instead of spaces.
        """
        return slugify(self.NAME)

    def __post_init__(self) -> None:
        # Check if the ALLOWED_CORS_ORIGINS is a string.
        if isinstance(self.ALLOWED_CORS_ORIGINS, str):
            # Check if the string starts with "[" and ends with "]", indicating a list.
            if self.ALLOWED_CORS_ORIGINS.startswith("[") and self.ALLOWED_CORS_ORIGINS.endswith("]"):
                try:
                    # Safely evaluate the string as a Python list.
                    self.ALLOWED_CORS_ORIGINS = json.loads(self.ALLOWED_CORS_ORIGINS)
                except (SyntaxError, ValueError):
                    # Handle potential errors if the string is not a valid Python literal.
                    msg = "ALLOWED_CORS_ORIGINS is not a valid list representation."
                    raise ValueError(msg) from None
            else:
                # Split the string by commas into a list if it is not meant to be a list representation.
                self.ALLOWED_CORS_ORIGINS = [host.strip() for host in self.ALLOWED_CORS_ORIGINS.split(",")]


@dataclass
class Settings:
    app: AppSettings = field(default_factory=AppSettings)
    db: DatabaseSettings = field(default_factory=DatabaseSettings)
