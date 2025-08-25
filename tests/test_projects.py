"""
Tests for the ProjectsResource class.
"""

import pytest
from unittest.mock import Mock
from beagle_sdk.resources.projects import ProjectsResource


class TestProjectsResource:
    """Test cases for ProjectsResource."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.projects = ProjectsResource(self.mock_client)
    
    def test_list_projects(self):
        """Test listing all projects."""
        expected_response = {'data': [{'id': '1', 'name': 'Test Project'}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.list()
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/projects', params={})
    
    def test_list_projects_with_search(self):
        """Test listing projects with search parameter."""
        expected_response = {'data': [{'id': '1', 'name': 'Test Project'}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.list(search='test')
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/projects', params={'search': 'test'})
    
    def test_get_project(self):
        """Test getting a specific project."""
        project_key = 'project-uuid'
        expected_response = {'id': project_key, 'name': 'Test Project'}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get(project_key)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with(f'/rest/v3/project/{project_key}')
    
    def test_create_project(self):
        """Test creating a new project."""
        project_data = {'name': 'New Project', 'description': 'Test project'}
        expected_response = {'id': 'new-uuid', **project_data}
        self.mock_client.post.return_value = expected_response
        
        result = self.projects.create(project_data)
        
        assert result == expected_response
        self.mock_client.post.assert_called_once_with('/rest/v3/project', data=project_data)
    
    def test_update_project(self):
        """Test updating an existing project."""
        project_data = {'id': 'project-uuid', 'name': 'Updated Project'}
        expected_response = project_data
        self.mock_client.put.return_value = expected_response
        
        result = self.projects.update(project_data)
        
        assert result == expected_response
        self.mock_client.put.assert_called_once_with('/rest/v3/project', data=project_data)
    
    def test_delete_project(self):
        """Test deleting a project."""
        project_key = 'project-uuid'
        expected_response = {'message': 'Project deleted'}
        self.mock_client.delete.return_value = expected_response
        
        result = self.projects.delete(project_key)
        
        assert result == expected_response
        self.mock_client.delete.assert_called_once_with('/rest/v3/project', params={'project_key': project_key})
    
    def test_get_webhook(self):
        """Test getting project webhook."""
        project_key = 'project-uuid'
        expected_response = {'url': 'https://example.com/webhook', 'active': True}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_webhook(project_key)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with(f'/rest/v3/project/{project_key}/webhook')
    
    def test_create_webhook(self):
        """Test creating project webhook."""
        project_key = 'project-uuid'
        webhook_data = {'url': 'https://example.com/webhook', 'events': ['test_completed']}
        expected_response = {'id': 'webhook-id', **webhook_data}
        self.mock_client.post.return_value = expected_response
        
        result = self.projects.create_webhook(project_key, webhook_data)
        
        assert result == expected_response
        self.mock_client.post.assert_called_once_with(f'/rest/v3/project/{project_key}/webhook', data=webhook_data)
    
    def test_delete_webhook(self):
        """Test deleting project webhook."""
        project_key = 'project-uuid'
        expected_response = {'message': 'Webhook deleted'}
        self.mock_client.delete.return_value = expected_response
        
        result = self.projects.delete_webhook(project_key)
        
        assert result == expected_response
        self.mock_client.delete.assert_called_once_with(f'/rest/v3/project/{project_key}/webhook')
    
    def test_get_summary(self):
        """Test getting project summary."""
        project_key = 'project-uuid'
        expected_response = {'total_applications': 5, 'total_vulnerabilities': 10}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_summary(project_key)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/project/result/summary', params={'project_key': project_key})
    
    def test_get_all_summaries(self):
        """Test getting all project summaries."""
        expected_response = {'data': [{'project_id': '1', 'total_vulnerabilities': 5}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_all_summaries()
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/projects/result/summary')
    
    def test_get_open_count_by_criticality_with_project(self):
        """Test getting open count by criticality for a specific project."""
        project_key = 'project-uuid'
        expected_response = {'data': {'critical': 2, 'high': 5, 'medium': 10, 'low': 20}}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_open_count_by_criticality(project_key)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/projects/result/opencount/criticality', 
                                                   params={'project_key': project_key})
    
    def test_get_open_count_by_criticality_all_projects(self):
        """Test getting open count by criticality for all projects."""
        expected_response = {'data': [{'project_id': '1', 'critical': 2, 'high': 5}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_open_count_by_criticality()
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/projects/result/opencount/criticality')
    
    def test_get_score_with_project(self):
        """Test getting score for a specific project."""
        project_key = 'project-uuid'
        score_type = 'cvss'
        expected_response = {'score': 7.5}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_score(score_type, project_key)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/project/result/score', 
                                                   params={'score_type': score_type, 'project_key': project_key})
    
    def test_get_score_all_projects(self):
        """Test getting score for all projects."""
        score_type = 'cvss'
        expected_response = {'data': [{'project_id': '1', 'score': 7.5}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_score(score_type)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/projects/result/score', 
                                                   params={'score_type': score_type})
    
    def test_get_score_trend_with_limit(self):
        """Test getting score trend with limit."""
        score_type = 'cvss'
        limit = 10
        expected_response = {'data': [{'date': '2024-01-01', 'score': 7.5}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_score_trend(score_type, limit=limit)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/projects/result/trend/score', 
                                                   params={'score_type': score_type, 'limit': limit})
    
    def test_get_vulnerability_count_trend_with_project(self):
        """Test getting vulnerability count trend for a specific project."""
        project_key = 'project-uuid'
        expected_response = {'data': [{'date': '2024-01-01', 'count': 5}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_vulnerability_count_trend(project_key)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/project/result/trend/vulnerabilitycount', 
                                                   params={'project_key': project_key})
    
    def test_get_insight_with_project(self):
        """Test getting insights for a specific project."""
        project_key = 'project-uuid'
        expected_response = {'recommendations': ['Fix critical issues'], 'security_score': 85}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_insight(project_key)
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/project/result/insight', 
                                                   params={'project_key': project_key})
    
    def test_get_insight_all_projects(self):
        """Test getting insights for all projects."""
        expected_response = {'data': [{'project_id': '1', 'security_score': 85}]}
        self.mock_client.get.return_value = expected_response
        
        result = self.projects.get_insight()
        
        assert result == expected_response
        self.mock_client.get.assert_called_once_with('/rest/v3/projects/result/insight')
