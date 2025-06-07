"""
Core exceptions for the Affiliate Matrix backend.

This module defines custom exception classes that can be used throughout the application
for consistent error handling and reporting.
"""

from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException, status


class AffiliateMatrixException(Exception):
    """Base exception class for all Affiliate Matrix exceptions."""
    
    def __init__(self, message: str = "An error occurred"):
        self.message = message
        super().__init__(self.message)


class ItemNotFoundError(AffiliateMatrixException):
    """Exception raised when a requested item is not found."""
    
    def __init__(self, item_type: str, item_id: Union[str, int]):
        self.item_type = item_type
        self.item_id = item_id
        self.message = f"{item_type} with id {item_id} not found"
        super().__init__(self.message)


class ValidationError(AffiliateMatrixException):
    """Exception raised when data validation fails."""
    
    def __init__(self, message: str = "Validation error", errors: Optional[List[Dict[str, Any]]] = None):
        self.errors = errors or []
        self.message = message
        super().__init__(self.message)


class DatabaseError(AffiliateMatrixException):
    """Exception raised when a database operation fails."""
    
    def __init__(self, message: str = "Database error", details: Optional[str] = None):
        self.details = details
        self.message = message
        super().__init__(self.message)


class ConnectionError(AffiliateMatrixException):
    """Exception raised when a connection operation fails."""
    
    def __init__(self, connection_id: str, message: str = "Connection error", details: Optional[str] = None):
        self.connection_id = connection_id
        self.details = details
        self.message = message
        super().__init__(self.message)


class AuthenticationError(AffiliateMatrixException):
    """Exception raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        self.message = message
        super().__init__(self.message)


class AuthorizationError(AffiliateMatrixException):
    """Exception raised when a user is not authorized to perform an action."""
    
    def __init__(self, message: str = "Not authorized to perform this action"):
        self.message = message
        super().__init__(self.message)


class ConfigurationError(AffiliateMatrixException):
    """Exception raised when there is a configuration error."""
    
    def __init__(self, message: str = "Configuration error", config_key: Optional[str] = None):
        self.config_key = config_key
        self.message = message
        if config_key:
            self.message = f"{message} (key: {config_key})"
        super().__init__(self.message)


class ExternalServiceError(AffiliateMatrixException):
    """Exception raised when an external service call fails."""
    
    def __init__(self, service_name: str, message: str = "External service error", details: Optional[str] = None):
        self.service_name = service_name
        self.details = details
        self.message = f"{message} ({service_name})"
        super().__init__(self.message)


class RateLimitError(AffiliateMatrixException):
    """Exception raised when rate limits are exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        self.retry_after = retry_after
        self.message = message
        if retry_after:
            self.message = f"{message} (retry after {retry_after} seconds)"
        super().__init__(self.message)
