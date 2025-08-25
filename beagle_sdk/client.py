"""
Main client class for the Beagle SDK.
"""

import requests
import time
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin, urlencode

from .exceptions import (
    BeagleAPIError,
    BeagleAuthenticationError,
    BeagleValidationError,
    BeagleNotFoundError,
    BeagleRateLimitError,
    BeagleServerError,
)
from .resources.projects import ProjectsResource
from .resources.applications import ApplicationsResource
from .resources.testing import TestingResource
from .resources.results import ResultsResource


class BeagleClient:
    """
    Main client class for interacting with the Beagle v3 API.
    
    Args:
        api_key (str): Your Beagle API key
        base_url (str, optional): Base URL for the API. Defaults to production URL.
        timeout (int, optional): Request timeout in seconds. Defaults to 30.
        max_retries (int, optional): Maximum number of retries for failed requests. Defaults to 3.
    """
    
    DEFAULT_BASE_URL = "https://api.beagle.security"
    DEFAULT_TIMEOUT = 30
    DEFAULT_MAX_RETRIES = 3
    
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Initialize session
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'beagle-python-sdk/1.0.0'
        })
        
        # Initialize resource classes
        self.projects = ProjectsResource(self)
        self.applications = ApplicationsResource(self)
        self.testing = TestingResource(self)
        self.results = ResultsResource(self)
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions for errors."""
        
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                # Handle non-JSON responses (e.g., PDF downloads)
                return {'content': response.content, 'headers': dict(response.headers)}
        
        # Handle error responses
        try:
            error_data = response.json()
            error_message = error_data.get('message', f'HTTP {response.status_code}')
        except ValueError:
            error_message = f'HTTP {response.status_code}: {response.text}'
        
        if response.status_code == 401:
            raise BeagleAuthenticationError(error_message, response.status_code, response)
        elif response.status_code == 400:
            raise BeagleValidationError(error_message, response.status_code, response)
        elif response.status_code == 404:
            raise BeagleNotFoundError(error_message, response.status_code, response)
        elif response.status_code == 429:
            raise BeagleRateLimitError(error_message, response.status_code, response)
        elif response.status_code >= 500:
            raise BeagleServerError(error_message, response.status_code, response)
        else:
            raise BeagleAPIError(error_message, response.status_code, response)
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request with retry logic."""
        
        url = urljoin(self.base_url, endpoint)
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        # Add query parameters to URL if provided
        if params:
            url += '?' + urlencode(params)
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=request_headers,
                    timeout=self.timeout
                )
                
                return self._handle_response(response)
                
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt == self.max_retries:
                    raise BeagleAPIError(f"Connection failed after {self.max_retries + 1} attempts: {str(e)}")
                
                # Exponential backoff
                time.sleep(2 ** attempt)
                continue
            except BeagleRateLimitError:
                if attempt == self.max_retries:
                    raise
                
                # Wait longer for rate limits
                time.sleep(60)
                continue
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return self._make_request('POST', endpoint, params=params, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request."""
        return self._make_request('PUT', endpoint, params=params, data=data)
    
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._make_request('DELETE', endpoint, params=params)
