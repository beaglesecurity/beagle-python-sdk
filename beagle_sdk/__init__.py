"""
Beagle Python SDK - A production-ready SDK for the Beagle v3 API.

This SDK provides easy access to all Beagle v3 API endpoints including:
- Project management
- Application management  
- Testing operations
- Result retrieval
- Webhook management
"""

from .client import BeagleClient
from .exceptions import (
    BeagleAPIError,
    BeagleAuthenticationError,
    BeagleValidationError,
    BeagleNotFoundError,
    BeagleRateLimitError,
)

__version__ = "1.0.0"
__author__ = "Beagle Team"
__email__ = "support@beagle.security"

__all__ = [
    "BeagleClient",
    "BeagleAPIError",
    "BeagleAuthenticationError", 
    "BeagleValidationError",
    "BeagleNotFoundError",
    "BeagleRateLimitError",
]
