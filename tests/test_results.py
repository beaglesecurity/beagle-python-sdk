"""
Tests for the ResultsResource class.
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch, mock_open
from beagle_sdk.resources.results import ResultsResource


class TestResultsResource:
    """Test cases for ResultsResource."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.results = ResultsResource(self.mock_client)
    
    def test_get_json_latest(self):
        """Test getting latest JSON results."""
        app_token = 'app-token-123'
        expected_response = {'vulnerabilities': [{'id': '1', 'title': 'XSS'}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.results.get_json(app_token)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/result/json', 
                                                   params={'application_token': app_token})
    
    def test_get_json_with_result_token(self):
        """Test getting JSON results for specific test session."""
        app_token = 'app-token-123'
        result_token = 'result-token-123'
        expected_response = {'vulnerabilities': [{'id': '1', 'title': 'XSS'}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.results.get_json(app_token, result_token)
        
        assert result == expected_response
        expected_params = {
            'application_token': app_token,
            'result_token': result_token
        }
        self.mock_client.get.assert_called_once_with('/rest/v3/result/json', params=expected_params)
    
    def test_get_pdf_latest(self):
        """Test getting latest PDF report."""
        app_token = 'app-token-123'
        expected_response = {'content': b'PDF content', 'headers': {'content-type': 'application/pdf'}}
        self.mock_client.get.return_value = expected_response
        
        result = self.results.get_pdf(app_token)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/result/pdf', 
                                                   params={'application_token': app_token})
    
    def test_get_pdf_with_result_token(self):
        """Test getting PDF report for specific test session."""
        app_token = 'app-token-123'
        result_token = 'result-token-123'
        expected_response = {'content': b'PDF content', 'headers': {'content-type': 'application/pdf'}}
        self.mock_client.get.return_value = expected_response
        
        result = self.results.get_pdf(app_token, result_token)
        
        assert result == expected_response
        expected_params = {
            'application_token': app_token,
            'result_token': result_token
        }
        self.mock_client.get.assert_called_once_with('/rest/v3/report/pdf', params=expected_params)
    
    def test_download_pdf_with_custom_path(self):
        """Test downloading PDF with custom output path."""
        app_token = 'app-token-123'
        result_token = 'result-token-123'
        output_path = '/tmp/custom_report.pdf'
        
        mock_response = {'content': b'PDF content'}
        self.mock_client.get.return_value = mock_response
        
        with patch('builtins.open', mock_open()) as mock_file:
            result_path = self.results.download_pdf(app_token, result_token, output_path)
        
        assert result_path == output_path
        mock_file.assert_called_once_with(output_path, 'wb')
        mock_file().write.assert_called_once_with(b'PDF content')
    
    def test_download_pdf_auto_filename_with_result_token(self):
        """Test downloading PDF with auto-generated filename (with result token)."""
        app_token = 'app-token-123'
        result_token = 'result-token-456'
        
        mock_response = {'content': b'PDF content'}
        self.mock_client.get.return_value = mock_response
        
        with patch('builtins.open', mock_open()) as mock_file:
            result_path = self.results.download_pdf(app_token, result_token)
        
        expected_path = f"beagle_report_{app_token[:8]}_{result_token[:8]}.pdf"
        assert result_path == expected_path
        mock_file.assert_called_once_with(expected_path, 'wb')
    
    def test_download_pdf_auto_filename_latest(self):
        """Test downloading PDF with auto-generated filename (latest)."""
        app_token = 'app-token-123'
        
        mock_response = {'content': b'PDF content'}
        self.mock_client.get.return_value = mock_response
        
        with patch('builtins.open', mock_open()) as mock_file:
            result_path = self.results.download_pdf(app_token)
        
        expected_path = f"beagle_report_{app_token[:8]}_latest.pdf"
        assert result_path == expected_path
        mock_file.assert_called_once_with(expected_path, 'wb')
    
    def test_download_pdf_calls_get_pdf_correctly(self):
        """Test that download_pdf calls get_pdf with correct parameters."""
        app_token = 'app-token-123'
        result_token = 'result-token-456'
        
        mock_response = {'content': b'PDF content'}
        self.mock_client.get.return_value = mock_response
        
        with patch('builtins.open', mock_open()):
            self.results.download_pdf(app_token, result_token)
        
        # Verify get_pdf was called with the right endpoint
        expected_params = {
            'application_token': app_token,
            'result_token': result_token
        }
        self.mock_client.get.assert_called_once_with('/rest/v3/report/pdf', params=expected_params)
