"""
Tests for the BeagleClient class.
"""

import pytest
import requests
from unittest.mock import Mock, patch
from beagle_sdk import BeagleClient
from beagle_sdk.exceptions import (
    BeagleAPIError,
    BeagleAuthenticationError,
    BeagleValidationError,
    BeagleNotFoundError,
    BeagleRateLimitError,
    BeagleServerError,
)


class TestBeagleClient:
    """Test cases for BeagleClient."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.api_key = "test-api-key"
        self.client = BeagleClient(api_key=self.api_key)
    
    def test_client_initialization(self):
        """Test client initialization with default values."""
        assert self.client.api_key == self.api_key
        assert self.client.base_url == BeagleClient.DEFAULT_BASE_URL
        assert self.client.timeout == BeagleClient.DEFAULT_TIMEOUT
        assert self.client.max_retries == BeagleClient.DEFAULT_MAX_RETRIES
        
        # Check session headers
        assert self.client.session.headers['Authorization'] == f'Bearer {self.api_key}'
        assert self.client.session.headers['Content-Type'] == 'application/json'
        assert 'beagle-python-sdk' in self.client.session.headers['User-Agent']
    
    def test_client_initialization_custom_values(self):
        """Test client initialization with custom values."""
        custom_client = BeagleClient(
            api_key="custom-key",
            base_url="https://custom.beagle.security",
            timeout=60,
            max_retries=5
        )
        
        assert custom_client.api_key == "custom-key"
        assert custom_client.base_url == "https://custom.beagle.security"
        assert custom_client.timeout == 60
        assert custom_client.max_retries == 5
    
    def test_base_url_trailing_slash_removed(self):
        """Test that trailing slash is removed from base URL."""
        client = BeagleClient(
            api_key="test",
            base_url="https://api.beagle.security/"
        )
        assert client.base_url == "https://api.beagle.security"
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_successful_response(self, mock_request):
        """Test handling of successful responses."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_request.return_value = mock_response
        
        result = self.client.get('/test')
        
        assert result == {'data': 'test'}
        mock_request.assert_called_once()
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_non_json_response(self, mock_request):
        """Test handling of non-JSON responses (e.g., PDF downloads)."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("No JSON object could be decoded")
        mock_response.content = b'PDF content'
        mock_response.headers = {'content-type': 'application/pdf'}
        mock_request.return_value = mock_response
        
        result = self.client.get('/test')
        
        assert result == {
            'content': b'PDF content',
            'headers': {'content-type': 'application/pdf'}
        }
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_authentication_error(self, mock_request):
        """Test handling of 401 authentication errors."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'message': 'Invalid API key'}
        mock_request.return_value = mock_response
        
        with pytest.raises(BeagleAuthenticationError) as exc_info:
            self.client.get('/test')
        
        assert str(exc_info.value) == 'Invalid API key'
        assert exc_info.value.status_code == 401
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_validation_error(self, mock_request):
        """Test handling of 400 validation errors."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'message': 'Invalid request data'}
        mock_request.return_value = mock_response
        
        with pytest.raises(BeagleValidationError) as exc_info:
            self.client.get('/test')
        
        assert str(exc_info.value) == 'Invalid request data'
        assert exc_info.value.status_code == 400
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_not_found_error(self, mock_request):
        """Test handling of 404 not found errors."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'message': 'Resource not found'}
        mock_request.return_value = mock_response
        
        with pytest.raises(BeagleNotFoundError) as exc_info:
            self.client.get('/test')
        
        assert str(exc_info.value) == 'Resource not found'
        assert exc_info.value.status_code == 404
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_rate_limit_error(self, mock_request):
        """Test handling of 429 rate limit errors."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {'message': 'Rate limit exceeded'}
        mock_request.return_value = mock_response
        
        with pytest.raises(BeagleRateLimitError) as exc_info:
            self.client.get('/test')
        
        assert str(exc_info.value) == 'Rate limit exceeded'
        assert exc_info.value.status_code == 429
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_server_error(self, mock_request):
        """Test handling of 5xx server errors."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'message': 'Internal server error'}
        mock_request.return_value = mock_response
        
        with pytest.raises(BeagleServerError) as exc_info:
            self.client.get('/test')
        
        assert str(exc_info.value) == 'Internal server error'
        assert exc_info.value.status_code == 500
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_generic_error(self, mock_request):
        """Test handling of other HTTP errors."""
        mock_response = Mock()
        mock_response.status_code = 418  # I'm a teapot
        mock_response.json.return_value = {'message': "I'm a teapot"}
        mock_request.return_value = mock_response
        
        with pytest.raises(BeagleAPIError) as exc_info:
            self.client.get('/test')
        
        assert str(exc_info.value) == "I'm a teapot"
        assert exc_info.value.status_code == 418
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_error_without_json(self, mock_request):
        """Test handling of errors without JSON response."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.side_effect = ValueError("No JSON")
        mock_response.text = "Internal Server Error"
        mock_request.return_value = mock_response
        
        with pytest.raises(BeagleServerError) as exc_info:
            self.client.get('/test')
        
        assert str(exc_info.value) == 'HTTP 500: Internal Server Error'
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_connection_error_retry(self, mock_request):
        """Test retry logic for connection errors."""
        mock_request.side_effect = [
            requests.exceptions.ConnectionError("Connection failed"),
            requests.exceptions.ConnectionError("Connection failed"),
            Mock(status_code=200, json=lambda: {'data': 'success'})
        ]
        
        with patch('beagle_sdk.client.time.sleep') as mock_sleep:
            result = self.client.get('/test')
        
        assert result == {'data': 'success'}
        assert mock_request.call_count == 3
        assert mock_sleep.call_count == 2  # Exponential backoff calls
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_connection_error_max_retries(self, mock_request):
        """Test max retries exceeded for connection errors."""
        mock_request.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        with patch('beagle_sdk.client.time.sleep'):
            with pytest.raises(BeagleAPIError) as exc_info:
                self.client.get('/test')
        
        assert "Connection failed after" in str(exc_info.value)
        assert mock_request.call_count == self.client.max_retries + 1
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_rate_limit_retry(self, mock_request):
        """Test retry logic for rate limit errors."""
        rate_limit_response = Mock()
        rate_limit_response.status_code = 429
        rate_limit_response.json.return_value = {'message': 'Rate limit exceeded'}
        
        success_response = Mock()
        success_response.status_code = 200
        success_response.json.return_value = {'data': 'success'}
        
        mock_request.side_effect = [rate_limit_response, success_response]
        
        with patch('beagle_sdk.client.time.sleep') as mock_sleep:
            result = self.client.get('/test')
        
        assert result == {'data': 'success'}
        assert mock_request.call_count == 2
        mock_sleep.assert_called_once_with(60)  # Rate limit backoff
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_get_method(self, mock_request):
        """Test GET method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_request.return_value = mock_response
        
        self.client.get('/test', params={'key': 'value'})
        
        args, kwargs = mock_request.call_args
        assert kwargs['method'] == 'GET'
        assert '/test?key=value' in kwargs['url']
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_post_method(self, mock_request):
        """Test POST method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_request.return_value = mock_response
        
        data = {'key': 'value'}
        self.client.post('/test', data=data, params={'param': 'value'})
        
        args, kwargs = mock_request.call_args
        assert kwargs['method'] == 'POST'
        assert kwargs['json'] == data
        assert '/test?param=value' in kwargs['url']
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_put_method(self, mock_request):
        """Test PUT method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_request.return_value = mock_response
        
        data = {'key': 'value'}
        self.client.put('/test', data=data)
        
        args, kwargs = mock_request.call_args
        assert kwargs['method'] == 'PUT'
        assert kwargs['json'] == data
    
    @patch('beagle_sdk.client.requests.Session.request')
    def test_delete_method(self, mock_request):
        """Test DELETE method."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_request.return_value = mock_response
        
        self.client.delete('/test', params={'id': '123'})
        
        args, kwargs = mock_request.call_args
        assert kwargs['method'] == 'DELETE'
        assert '/test?id=123' in kwargs['url']
