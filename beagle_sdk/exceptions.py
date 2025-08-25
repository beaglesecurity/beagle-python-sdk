"""
Exception classes for the Beagle SDK.
"""


class BeagleAPIError(Exception):
    """Base exception for all Beagle API errors."""
    
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class BeagleAuthenticationError(BeagleAPIError):
    """Exception raised for authentication errors (401)."""
    pass


class BeagleValidationError(BeagleAPIError):
    """Exception raised for validation errors (400)."""
    pass


class BeagleNotFoundError(BeagleAPIError):
    """Exception raised for not found errors (404)."""
    pass


class BeagleRateLimitError(BeagleAPIError):
    """Exception raised for rate limit errors (429)."""
    pass


class BeagleServerError(BeagleAPIError):
    """Exception raised for server errors (5xx)."""
    pass
