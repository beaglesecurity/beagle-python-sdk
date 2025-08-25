"""
Tests for the ApplicationsResource class.
"""

import pytest
from unittest.mock import Mock
from beagle_sdk.resources.applications import ApplicationsResource


class TestApplicationsResource:
    """Test cases for ApplicationsResource."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.applications = ApplicationsResource(self.mock_client)
    
    def test_list_applications_default(self):
        """Test listing applications with default parameters."""
        expected_response = {'data': [{'id': '1', 'name': 'Test App'}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.list()
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/applications', 
                                                   params={'page': 0, 'count': 20})
    
    def test_list_applications_with_parameters(self):
        """Test listing applications with custom parameters."""
        expected_response = {'data': [{'id': '1', 'name': 'Test App'}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.list(
            page=1, 
            count=50, 
            project_key='project-uuid',
            search='web',
            importance='high'
        )
        
        assert result == expected_response
        expected_params = {
            'page': 1,
            'count': 50,
            'project_key': 'project-uuid',
            'search': 'web',
            'importance': 'high'
        }
        self.mock_client.get.assert_called_once_with('/rest/v3/applications', params=expected_params)
    
    def test_get_application(self):
        """Test getting a specific application."""
        app_token = 'app-token-123'
        expected_response = {'application_token': app_token, 'name': 'Test App'}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.get(app_token)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/application', 
                                                   params={'application_token': app_token})
    
    def test_create_application(self):
        """Test creating a new application."""
        app_data = {'name': 'New App', 'url': 'https://example.com'}
        expected_response = {'application_token': 'new-token', **app_data}
        self.mock_client.post.return_value = expected_response
        
        result = self.applications.create(app_data)
        
        assert result == expected_response
        self.mock_client.post.assert_called_once_with('/rest/v3/application', data=app_data)
    
    def test_update_application(self):
        """Test updating an existing application."""
        app_data = {'application_token': 'app-token', 'name': 'Updated App'}
        expected_response = app_data
        self.mock_client.put.return_value = expected_response
        
        result = self.applications.update(app_data)
        
        assert result == expected_response
        self.mock_client.put.assert_called_once_with('/rest/v3/application', data=app_data)
    
    def test_delete_application(self):
        """Test deleting an application."""
        app_token = 'app-token-123'
        expected_response = {'message': 'Application deleted'}
        self.mock_client.delete.return_value = expected_response
        
        result = self.applications.delete(app_token)
        
        assert result == expected_response
        self.mock_client.delete.assert_called_once_with('/rest/v3/application', 
                                                      params={'application_token': app_token})
    
    def test_get_signature(self):
        """Test getting domain signature."""
        app_token = 'app-token-123'
        expected_response = {'signature': 'signature-value', 'domain': 'example.com'}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.get_signature(app_token)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/application/signature', 
                                                   params={'application_token': app_token})
    
    def test_verify_signature(self):
        """Test verifying signature."""
        app_token = 'app-token-123'
        signature_data = {'signature': 'signature-value'}
        expected_response = {'verified': True}
        self.mock_client.post.return_value = expected_response
        
        result = self.applications.verify_signature(app_token, signature_data)
        
        assert result == expected_response
        self.mock_client.post.assert_called_once_with('/rest/v3/application/signature', 
                                                    data=signature_data,
                                                    params={'application_token': app_token})
    
    def test_get_webhook(self):
        """Test getting application webhook."""
        app_token = 'app-token-123'
        expected_response = {'url': 'https://example.com/webhook', 'active': True}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.get_webhook(app_token)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/application/webhook', 
                                                   params={'application_token': app_token})
    
    def test_create_webhook(self):
        """Test creating application webhook."""
        app_token = 'app-token-123'
        webhook_data = {'url': 'https://example.com/webhook', 'events': ['test_completed']}
        expected_response = {'id': 'webhook-id', **webhook_data}
        self.mock_client.post.return_value = expected_response
        
        result = self.applications.create_webhook(app_token, webhook_data)
        
        assert result == expected_response
        self.mock_client.post.assert_called_once_with('/rest/v3/application/webhook', 
                                                    data=webhook_data,
                                                    params={'application_token': app_token})
    
    def test_delete_webhook(self):
        """Test deleting application webhook."""
        app_token = 'app-token-123'
        expected_response = {'message': 'Webhook deleted'}
        self.mock_client.delete.return_value = expected_response
        
        result = self.applications.delete_webhook(app_token)
        
        assert result == expected_response
        self.mock_client.delete.assert_called_once_with('/rest/v3/application/webhook', 
                                                      params={'application_token': app_token})
    
    def test_get_summary(self):
        """Test getting application summary."""
        app_token = 'app-token-123'
        expected_response = {'total_vulnerabilities': 10, 'critical_count': 2}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.get_summary(app_token)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/application/result/summary', 
                                                   params={'application_token': app_token})
    
    def test_get_open_count_by_criticality(self):
        """Test getting open count by criticality."""
        app_token = 'app-token-123'
        expected_response = {'data': {'critical': 2, 'high': 5, 'medium': 10, 'low': 20}}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.get_open_count_by_criticality(app_token)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/application/result/opencount/criticality', 
                                                   params={'application_token': app_token})
    
    def test_get_open_count_by_catalog(self):
        """Test getting open count by catalog."""
        app_token = 'app-token-123'
        expected_response = {'data': {'new': 5, 'reopened': 2, 'not_fixed': 8, 'fixed': 15}}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.get_open_count_by_catalog(app_token)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/application/result/opencount/catalog', 
                                                   params={'application_token': app_token})
    
    def test_get_score(self):
        """Test getting application score."""
        app_token = 'app-token-123'
        score_type = 'cvss'
        expected_response = {'score': 7.5}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.get_score(app_token, score_type)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/application/result/score', 
                                                   params={'application_token': app_token, 'score_type': score_type})
    
    def test_get_score_trend(self):
        """Test getting score trend."""
        app_token = 'app-token-123'
        score_type = 'cvss'
        expected_response = {'data': [{'date': '2024-01-01', 'score': 7.5}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.get_score_trend(app_token, score_type)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/application/result/trend/score', 
                                                   params={'application_token': app_token, 'score_type': score_type})
    
    def test_get_vulnerability_count_trend(self):
        """Test getting vulnerability count trend."""
        app_token = 'app-token-123'
        expected_response = {'data': [{'date': '2024-01-01', 'count': 5}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.get_vulnerability_count_trend(app_token)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/application/result/trend/vulnerabilitycount', 
                                                   params={'application_token': app_token})
    
    def test_get_insight(self):
        """Test getting application insights."""
        app_token = 'app-token-123'
        expected_response = {'recommendations': ['Fix critical issues'], 'security_score': 85}
        self.mock_client.get.return_value = expected_response
        
        result = self.applications.get_insight(app_token)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/applications/result/insight', 
                                                   params={'application_token': app_token})
