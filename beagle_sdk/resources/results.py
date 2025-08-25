"""
Results resource for the Beagle SDK.
"""

from typing import Dict, Any, Optional


class ResultsResource:
    """Resource for retrieving test results."""
    
    def __init__(self, client):
        self.client = client
    
    def get_json(self, application_token: str, result_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the JSON format VAPT result.
        
        Args:
            application_token (str): The application token
            result_token (str, optional): The result token for a specific session.
                                        If None, gets latest test result.
            
        Returns:
            Dict containing JSON formatted test results
        """
        params = {'application_token': application_token}
        if result_token:
            params['result_token'] = result_token
            
        return self.client.get('/rest/v3/result/json', params=params)
    
    def get_pdf(self, application_token: str, result_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Download the PDF report.
        
        Args:
            application_token (str): The application token
            result_token (str, optional): The result token for a specific session.
                                        If None, gets latest test result.
            
        Returns:
            Dict containing PDF content and headers
        """
        params = {'application_token': application_token}
        if result_token:
            params['result_token'] = result_token
            endpoint = '/rest/v3/report/pdf'
        else:
            endpoint = '/rest/v3/result/pdf'
            
        return self.client.get(endpoint, params=params)
    
    def download_pdf(self, application_token: str, result_token: Optional[str] = None, output_path: Optional[str] = None) -> str:
        """
        Download the PDF report and save to file.
        
        Args:
            application_token (str): The application token
            result_token (str, optional): The result token for a specific session
            output_path (str, optional): Path to save the PDF file.
                                       If None, generates filename automatically.
            
        Returns:
            str: Path to the saved PDF file
        """
        response = self.get_pdf(application_token, result_token)
        
        if output_path is None:
            # Generate filename
            if result_token:
                output_path = f"beagle_report_{application_token[:8]}_{result_token[:8]}.pdf"
            else:
                output_path = f"beagle_report_{application_token[:8]}_latest.pdf"
        
        # Write PDF content to file
        with open(output_path, 'wb') as f:
            f.write(response['content'])
        
        return output_path
