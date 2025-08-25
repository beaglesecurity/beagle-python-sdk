"""
Application resource for the Beagle SDK.
"""

from typing import Dict, Any, Optional, List


class ApplicationsResource:
    """Resource for managing applications."""
    
    def __init__(self, client):
        self.client = client
    
    def list(
        self, 
        page: int = 0, 
        count: int = 20, 
        project_key: Optional[str] = None,
        search: Optional[str] = None,
        importance: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get all applications from the account or under a specific project.
        
        Args:
            page (int): Page number for pagination (default: 0)
            count (int): Number of items per page (default: 20)
            project_key (str, optional): Filter by project key
            search (str, optional): Search text to filter applications
            importance (str, optional): Filter by importance level (e.g., 'high')
            
        Returns:
            Dict containing list of applications
        """
        params = {'page': page, 'count': count}
        
        if project_key:
            params['project_key'] = project_key
        if search:
            params['search'] = search
        if importance:
            params['importance'] = importance
            
        return self.client.get('/rest/v3/applications', params=params)
    
    def get(self, application_token: str) -> Dict[str, Any]:
        """
        Get details of an application using an application token.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing application details
        """
        params = {'application_token': application_token}
        return self.client.get('/rest/v3/application', params=params)
    
    def create(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new application.
        
        Args:
            application_data (dict): Application data to create
            
        Returns:
            Dict containing created application details
        """
        return self.client.post('/rest/v3/application', data=application_data)
    
    def update(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modify an existing application.
        
        Args:
            application_data (dict): Application data to update
            
        Returns:
            Dict containing updated application details
        """
        return self.client.put('/rest/v3/application', data=application_data)
    
    def delete(self, application_token: str) -> Dict[str, Any]:
        """
        Delete an application.
        
        Args:
            application_token (str): The application token to delete
            
        Returns:
            Dict containing deletion confirmation
        """
        params = {'application_token': application_token}
        return self.client.delete('/rest/v3/application', params=params)
    
    def get_signature(self, application_token: str) -> Dict[str, Any]:
        """
        Get domain signature for an application.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing domain signature
        """
        params = {'application_token': application_token}
        return self.client.get('/rest/v3/application/signature', params=params)
    
    def verify_signature(self, application_token: str, signature_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify signature for an application.
        
        Args:
            application_token (str): The application token
            signature_data (dict): Signature data to verify
            
        Returns:
            Dict containing signature verification result
        """
        params = {'application_token': application_token}
        return self.client.post('/rest/v3/application/signature', data=signature_data, params=params)
    
    # Webhook methods
    def get_webhook(self, application_token: str) -> Dict[str, Any]:
        """
        Get webhook configuration for an application.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing webhook configuration
        """
        params = {'application_token': application_token}
        return self.client.get('/rest/v3/application/webhook', params=params)
    
    def create_webhook(self, application_token: str, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a webhook for an application.
        
        Args:
            application_token (str): The application token
            webhook_data (dict): Webhook configuration data
            
        Returns:
            Dict containing created webhook details
        """
        params = {'application_token': application_token}
        return self.client.post('/rest/v3/application/webhook', data=webhook_data, params=params)
    
    def delete_webhook(self, application_token: str) -> Dict[str, Any]:
        """
        Delete an application webhook.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing deletion confirmation
        """
        params = {'application_token': application_token}
        return self.client.delete('/rest/v3/application/webhook', params=params)
    
    # Result summary methods
    def get_summary(self, application_token: str) -> Dict[str, Any]:
        """
        Get result summary for an application.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing application summary
        """
        params = {'application_token': application_token}
        return self.client.get('/rest/v3/application/result/summary', params=params)
    
    def get_open_count_by_criticality(self, application_token: str) -> Dict[str, Any]:
        """
        Get open count by criticality for an application.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing open count by criticality
        """
        params = {'application_token': application_token}
        return self.client.get('/rest/v3/application/result/opencount/criticality', params=params)
    
    def get_open_count_by_catalog(self, application_token: str) -> Dict[str, Any]:
        """
        Get open count by catalog (new, re-opened, not fixed, fixed) for an application.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing open count by catalog
        """
        params = {'application_token': application_token}
        return self.client.get('/rest/v3/application/result/opencount/catalog', params=params)
    
    def get_score(self, application_token: str, score_type: str) -> Dict[str, Any]:
        """
        Get score for an application.
        
        Args:
            application_token (str): The application token
            score_type (str): Type of score (e.g., 'cvss')
            
        Returns:
            Dict containing score information
        """
        params = {'application_token': application_token, 'score_type': score_type}
        return self.client.get('/rest/v3/application/result/score', params=params)
    
    def get_score_trend(self, application_token: str, score_type: str) -> Dict[str, Any]:
        """
        Get score trend for an application.
        
        Args:
            application_token (str): The application token
            score_type (str): Type of score (e.g., 'cvss')
            
        Returns:
            Dict containing score trend information
        """
        params = {'application_token': application_token, 'score_type': score_type}
        return self.client.get('/rest/v3/application/result/trend/score', params=params)
    
    def get_vulnerability_count_trend(self, application_token: str) -> Dict[str, Any]:
        """
        Get vulnerability count trend for an application.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing vulnerability count trend information
        """
        params = {'application_token': application_token}
        return self.client.get('/rest/v3/application/result/trend/vulnerabilitycount', params=params)
    
    def get_insight(self, application_token: str) -> Dict[str, Any]:
        """
        Get insights for an application.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing application insights
        """
        params = {'application_token': application_token}
        return self.client.get('/rest/v3/applications/result/insight', params=params)
