"""
Error handlers for the Affiliate Matrix backend.

This module defines exception handlers that convert custom exceptions
to appropriate HTTP responses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError

from .exceptions import (
    AffiliateMatrixException,
    ItemNotFoundError,
    ValidationError,
    DatabaseError,
    ConnectionError,
    AuthenticationError,
    AuthorizationError,
    ConfigurationError,
    ExternalServiceError,
    RateLimitError
)


async def affiliate_matrix_exception_handler(request: Request, exc: AffiliateMatrixException) -> JSONResponse:
    """
    Handle generic AffiliateMatrixException.
    Returns a 500 Internal Server Error response.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message}
    )


async def item_not_found_error_handler(request: Request, exc: ItemNotFoundError) -> JSONResponse:
    """
    Handle ItemNotFoundError.
    Returns a 404 Not Found response with information about the missing item.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": exc.message,
            "item_type": exc.item_type,
            "item_id": exc.item_id
        }
    )


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    Handle ValidationError.
    Returns a 422 Unprocessable Entity response with validation error details.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.message,
            "errors": exc.errors
        }
    )


async def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """
    Handle DatabaseError.
    Returns a 500 Internal Server Error response with database error details.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": exc.message,
            "details": exc.details
        }
    )


async def connection_error_handler(request: Request, exc: ConnectionError) -> JSONResponse:
    """
    Handle ConnectionError.
    Returns a 500 Internal Server Error response with connection error details.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": exc.message,
            "connection_id": exc.connection_id,
            "details": exc.details
        }
    )


async def authentication_error_handler(request: Request, exc: AuthenticationError) -> JSONResponse:
    """
    Handle AuthenticationError.
    Returns a 401 Unauthorized response.
    """
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message}
    )


async def authorization_error_handler(request: Request, exc: AuthorizationError) -> JSONResponse:
    """
    Handle AuthorizationError.
    Returns a 403 Forbidden response.
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.message}
    )


async def configuration_error_handler(request: Request, exc: ConfigurationError) -> JSONResponse:
    """
    Handle ConfigurationError.
    Returns a 500 Internal Server Error response with configuration error details.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": exc.message,
            "config_key": exc.config_key
        }
    )


async def external_service_error_handler(request: Request, exc: ExternalServiceError) -> JSONResponse:
    """
    Handle ExternalServiceError.
    Returns a 502 Bad Gateway response with external service error details.
    """
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "detail": exc.message,
            "service_name": exc.service_name,
            "details": exc.details
        }
    )


async def rate_limit_error_handler(request: Request, exc: RateLimitError) -> JSONResponse:
    """
    Handle RateLimitError.
    Returns a 429 Too Many Requests response with retry information.
    """
    response = JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": exc.message}
    )
    if exc.retry_after:
        response.headers["Retry-After"] = str(exc.retry_after)
    return response


async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle FastAPI's RequestValidationError.
    Returns a 422 Unprocessable Entity response with validation error details.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


async def pydantic_validation_error_handler(request: Request, exc: PydanticValidationError) -> JSONResponse:
    """
    Handle Pydantic's ValidationError.
    Returns a 422 Unprocessable Entity response with validation error details.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


def register_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI application.
    """
    app.add_exception_handler(AffiliateMatrixException, affiliate_matrix_exception_handler)
    app.add_exception_handler(ItemNotFoundError, item_not_found_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(DatabaseError, database_error_handler)
    app.add_exception_handler(ConnectionError, connection_error_handler)
    app.add_exception_handler(AuthenticationError, authentication_error_handler)
    app.add_exception_handler(AuthorizationError, authorization_error_handler)
    app.add_exception_handler(ConfigurationError, configuration_error_handler)
    app.add_exception_handler(ExternalServiceError, external_service_error_handler)
    app.add_exception_handler(RateLimitError, rate_limit_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(PydanticValidationError, pydantic_validation_error_handler)
