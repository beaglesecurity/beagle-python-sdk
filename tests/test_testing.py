"""
Tests for the TestingResource class.
"""

import pytest
from unittest.mock import Mock
from beagle_sdk.resources.testing import TestingResource


class TestTestingResource:
    """Test cases for TestingResource."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.testing = TestingResource(self.mock_client)
    
    def test_start_test_without_config(self):
        """Test starting a test without configuration."""
        app_token = 'app-token-123'
        expected_response = {'result_token': 'result-token-123', 'status': 'started'}
        self.mock_client.post.return_value = expected_response
        
        result = self.testing.start(app_token)
        
        assert result == expected_response
        self.mock_client.post.assert_called_once_with('/rest/v3/test/start', 
                                                    data=None,
                                                    params={'application_token': app_token})
    
    def test_start_test_with_config(self):
        """Test starting a test with configuration."""
        app_token = 'app-token-123'
        test_config = {'scan_type': 'full', 'max_duration': 3600}
        expected_response = {'result_token': 'result-token-123', 'status': 'started'}
        self.mock_client.post.return_value = expected_response
        
        result = self.testing.start(app_token, test_config)
        
        assert result == expected_response
        self.mock_client.post.assert_called_once_with('/rest/v3/test/start', 
                                                    data=test_config,
                                                    params={'application_token': app_token})
    
    def test_get_status(self):
        """Test getting test status."""
        app_token = 'app-token-123'
        result_token = 'result-token-123'
        expected_response = {'status': 'running', 'progress': 45}
        self.mock_client.get.return_value = expected_response
        
        result = self.testing.get_status(app_token, result_token)
        
        assert result == expected_response
        expected_params = {
            'application_token': app_token,
            'result_token': result_token
        }
        self.mock_client.get.assert_called_once_with('/rest/v3/test/status', params=expected_params)
    
    def test_stop_test(self):
        """Test stopping a test."""
        app_token = 'app-token-123'
        expected_response = {'message': 'Test stopped', 'status': 'stopped'}
        self.mock_client.post.return_value = expected_response
        
        result = self.testing.stop(app_token)
        
        assert result == expected_response
        self.mock_client.post.assert_called_once_with('/rest/v3/test/stop', 
                                                    params={'application_token': app_token})
    
    def test_pause_test(self):
        """Test pausing a test."""
        app_token = 'app-token-123'
        expected_response = {'message': 'Test paused', 'status': 'paused'}
        self.mock_client.post.return_value = expected_response
        
        result = self.testing.pause(app_token)
        
        assert result == expected_response
        self.mock_client.post.assert_called_once_with('/rest/v3/test/pause', 
                                                    params={'application_token': app_token})
    
    def test_resume_test(self):
        """Test resuming a test."""
        app_token = 'app-token-123'
        expected_response = {'message': 'Test resumed', 'status': 'running'}
        self.mock_client.post.return_value = expected_response
        
        result = self.testing.resume(app_token)
        
        assert result == expected_response
        self.mock_client.post.assert_called_once_with('/rest/v3/test/resume', 
                                                    params={'application_token': app_token})
    
    def test_get_sessions_default(self):
        """Test getting test sessions with default parameters."""
        app_token = 'app-token-123'
        expected_response = {'data': [{'id': '1', 'status': 'completed'}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.testing.get_sessions(app_token)
        
        assert result == expected_response
        expected_params = {
            'application_token': app_token,
            'page': 0,
            'count': 20
        }
        self.mock_client.get.assert_called_once_with('/rest/v3/test/sessions', params=expected_params)
    
    def test_get_sessions_with_pagination(self):
        """Test getting test sessions with custom pagination."""
        app_token = 'app-token-123'
        expected_response = {'data': [{'id': '1', 'status': 'completed'}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.testing.get_sessions(app_token, page=2, count=50)
        
        assert result == expected_response
        expected_params = {
            'application_token': app_token,
            'page': 2,
            'count': 50
        }
        self.mock_client.get.assert_called_once_with('/rest/v3/test/sessions', params=expected_params)
    
    def test_get_running_sessions(self):
        """Test getting running test sessions."""
        expected_response = {'data': [{'id': '1', 'status': 'running', 'application': 'app-1'}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.testing.get_running_sessions()
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/test/runningsessions')
