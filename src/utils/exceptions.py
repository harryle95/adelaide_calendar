"""Litestar-saqlalchemy exception types.

Also, defines functions that translate service and repository exceptions
into HTTP exceptions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.exceptions import IntegrityError
from litestar.exceptions import (
    HTTPException,
    InternalServerException,
    NotFoundException,
)
from litestar.exceptions.responses import create_exception_response
from litestar.repository.exceptions import ConflictError, NotFoundError, RepositoryError
from litestar.status_codes import HTTP_409_CONFLICT

if TYPE_CHECKING:
    from typing import Any

    from litestar.connection import Request
    from litestar.response import Response

__all__ = ()


class HTTPConflictException(HTTPException):
    """Request conflict with the current state of the target resource."""

    status_code = HTTP_409_CONFLICT


def exception_to_http_response(
    request: Request[Any, Any, Any],
    exc: Exception,
) -> Response:
    """Transform repository exceptions to HTTP exceptions.

    Args:
        request: The request that experienced the exception.
        exc: Exception raised during handling of the request.

    Returns:
        Exception response appropriate to the type of original exception.
    """
    if isinstance(exc, HTTPException):
        return create_exception_response(request, exc)
    http_exc: type[HTTPException]
    if isinstance(exc, NotFoundError):
        http_exc = NotFoundException
        return create_exception_response(request, http_exc(detail=str(exc.detail)))
    if isinstance(exc, ConflictError | RepositoryError | IntegrityError):
        http_exc = HTTPConflictException
        return create_exception_response(request, http_exc(detail=str(exc.detail)))
    http_exc = InternalServerException
    return create_exception_response(request, http_exc(detail=str(exc.__cause__)))
