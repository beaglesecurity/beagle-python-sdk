"""
Project resource for the Beagle SDK.
"""

from typing import Dict, Any, Optional, List


class ProjectsResource:
    """Resource for managing projects."""
    
    def __init__(self, client):
        self.client = client
    
    def list(self, search: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all projects from the account.
        
        Args:
            search (str, optional): Search text to filter projects
            
        Returns:
            Dict containing list of projects
        """
        params = {}
        if search:
            params['search'] = search
            
        return self.client.get('/rest/v3/projects', params=params)
    
    def get(self, project_key: str) -> Dict[str, Any]:
        """
        Get a specific project by key.
        
        Args:
            project_key (str): The project key/UUID
            
        Returns:
            Dict containing project details
        """
        return self.client.get(f'/rest/v3/project/{project_key}')
    
    def create(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            project_data (dict): Project data to create
            
        Returns:
            Dict containing created project details
        """
        return self.client.post('/rest/v3/project', data=project_data)
    
    def update(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modify an existing project.
        
        Args:
            project_data (dict): Project data to update
            
        Returns:
            Dict containing updated project details
        """
        return self.client.put('/rest/v3/project', data=project_data)
    
    def delete(self, project_key: str) -> Dict[str, Any]:
        """
        Delete a project.
        
        Args:
            project_key (str): The project key/UUID to delete
            
        Returns:
            Dict containing deletion confirmation
        """
        return self.client.delete('/rest/v3/project', params={'project_key': project_key})
    
    # Webhook methods
    def get_webhook(self, project_key: str) -> Dict[str, Any]:
        """
        Get webhook configuration for a project.
        
        Args:
            project_key (str): The project key/UUID
            
        Returns:
            Dict containing webhook configuration
        """
        return self.client.get(f'/rest/v3/project/{project_key}/webhook')
    
    def create_webhook(self, project_key: str, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a webhook for a project.
        
        Args:
            project_key (str): The project key/UUID
            webhook_data (dict): Webhook configuration data
            
        Returns:
            Dict containing created webhook details
        """
        return self.client.post(f'/rest/v3/project/{project_key}/webhook', data=webhook_data)
    
    def delete_webhook(self, project_key: str) -> Dict[str, Any]:
        """
        Delete a project webhook.
        
        Args:
            project_key (str): The project key/UUID
            
        Returns:
            Dict containing deletion confirmation
        """
        return self.client.delete(f'/rest/v3/project/{project_key}/webhook')
    
    # Result summary methods
    def get_summary(self, project_key: str) -> Dict[str, Any]:
        """
        Get result summary for a project.
        
        Args:
            project_key (str): The project key/UUID
            
        Returns:
            Dict containing project summary
        """
        return self.client.get('/rest/v3/project/result/summary', params={'project_key': project_key})
    
    def get_all_summaries(self) -> Dict[str, Any]:
        """
        Get result summaries for all projects in the account.
        
        Returns:
            Dict containing summaries for all projects
        """
        return self.client.get('/rest/v3/projects/result/summary')
    
    def get_open_count_by_criticality(self, project_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Get open count by criticality for a project or all projects.
        
        Args:
            project_key (str, optional): The project key/UUID. If None, gets data for all projects.
            
        Returns:
            Dict containing open count by criticality
        """
        if project_key:
            return self.client.get('/rest/v3/projects/result/opencount/criticality', 
                                 params={'project_key': project_key})
        else:
            return self.client.get('/rest/v3/projects/result/opencount/criticality')
    
    def get_open_count_by_catalog(self, project_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Get open count by catalog (new, re-opened, not fixed, fixed) for a project or all projects.
        
        Args:
            project_key (str, optional): The project key/UUID. If None, gets data for all projects.
            
        Returns:
            Dict containing open count by catalog
        """
        if project_key:
            return self.client.get('/rest/v3/project/result/opencount/catalog', 
                                 params={'project_key': project_key})
        else:
            return self.client.get('/rest/v3/projects/result/opencount/catalog')
    
    def get_score(self, score_type: str, project_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Get score for a project or all projects.
        
        Args:
            score_type (str): Type of score (e.g., 'cvss')
            project_key (str, optional): The project key/UUID. If None, gets data for all projects.
            
        Returns:
            Dict containing score information
        """
        params = {'score_type': score_type}
        if project_key:
            params['project_key'] = project_key
            return self.client.get('/rest/v3/project/result/score', params=params)
        else:
            return self.client.get('/rest/v3/projects/result/score', params=params)
    
    def get_score_trend(self, score_type: str, project_key: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get score trend for a project or all projects.
        
        Args:
            score_type (str): Type of score (e.g., 'cvss')
            project_key (str, optional): The project key/UUID. If None, gets data for all projects.
            limit (int, optional): Limit number of results
            
        Returns:
            Dict containing score trend information
        """
        params = {'score_type': score_type}
        if limit:
            params['limit'] = limit
            
        if project_key:
            params['project_key'] = project_key
            return self.client.get('/rest/v3/project/result/trend/score', params=params)
        else:
            return self.client.get('/rest/v3/projects/result/trend/score', params=params)
    
    def get_vulnerability_count_trend(self, project_key: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get vulnerability count trend for a project or all projects.
        
        Args:
            project_key (str, optional): The project key/UUID. If None, gets data for all projects.
            limit (int, optional): Limit number of results
            
        Returns:
            Dict containing vulnerability count trend information
        """
        params = {}
        if limit:
            params['limit'] = limit
            
        if project_key:
            params['project_key'] = project_key
            return self.client.get('/rest/v3/project/result/trend/vulnerabilitycount', params=params)
        else:
            return self.client.get('/rest/v3/projects/result/trend/vulnerabilitycount', params=params)
    
    def get_insight(self, project_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Get insights for a project or all projects.
        
        Args:
            project_key (str, optional): The project key/UUID. If None, gets data for all projects.
            
        Returns:
            Dict containing project insights
        """
        if project_key:
            return self.client.get('/rest/v3/project/result/insight', 
                                 params={'project_key': project_key})
        else:
            return self.client.get('/rest/v3/projects/result/insight')
