"""
Testing resource for the Beagle SDK.
"""

from typing import Dict, Any, Optional


class TestingResource:
    """Resource for managing tests."""
    
    def __init__(self, client):
        self.client = client
    
    def start(self, application_token: str, test_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Start a test for an application.
        
        Args:
            application_token (str): The application token
            test_config (dict, optional): Additional test configuration
            
        Returns:
            Dict containing test start response with result_token
        """
        params = {'application_token': application_token}
        return self.client.post('/rest/v3/test/start', data=test_config, params=params)
    
    def get_status(self, application_token: str, result_token: str) -> Dict[str, Any]:
        """
        Get test status for a running test.
        
        Args:
            application_token (str): The application token
            result_token (str): The result token from test start
            
        Returns:
            Dict containing test status information
        """
        params = {
            'application_token': application_token,
            'result_token': result_token
        }
        return self.client.get('/rest/v3/test/status', params=params)
    
    def stop(self, application_token: str) -> Dict[str, Any]:
        """
        Stop a running test.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing test stop confirmation
        """
        params = {'application_token': application_token}
        return self.client.post('/rest/v3/test/stop', params=params)
    
    def pause(self, application_token: str) -> Dict[str, Any]:
        """
        Pause a running test.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing test pause confirmation
        """
        params = {'application_token': application_token}
        return self.client.post('/rest/v3/test/pause', params=params)
    
    def resume(self, application_token: str) -> Dict[str, Any]:
        """
        Resume a paused test.
        
        Args:
            application_token (str): The application token
            
        Returns:
            Dict containing test resume confirmation
        """
        params = {'application_token': application_token}
        return self.client.post('/rest/v3/test/resume', params=params)
    
    def get_sessions(self, application_token: str, page: int = 0, count: int = 20) -> Dict[str, Any]:
        """
        Get test sessions under an application.
        
        Args:
            application_token (str): The application token
            page (int): Page number for pagination (default: 0)
            count (int): Number of items per page (default: 20)
            
        Returns:
            Dict containing list of test sessions
        """
        params = {
            'application_token': application_token,
            'page': page,
            'count': count
        }
        return self.client.get('/rest/v3/test/sessions', params=params)
    
    def get_running_sessions(self) -> Dict[str, Any]:
        """
        Get all running test sessions under the account.
        
        Returns:
            Dict containing list of running test sessions
        """
        return self.client.get('/rest/v3/test/runningsessions')
