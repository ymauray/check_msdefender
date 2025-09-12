"""Microsoft Defender API client."""

import requests
from check_msdefender.core.exceptions import DefenderAPIError


class DefenderClient:
    """Client for Microsoft Defender API."""
    
    def __init__(self, authenticator, timeout=5, region="eu3"):
        """Initialize with authenticator and optional region.
        
        Args:
            authenticator: Authentication provider
            timeout: Request timeout in seconds
            region: Geographic region (eu, eu3, us, uk)
        """
        self.authenticator = authenticator
        self.timeout = timeout
        self.region = region
        self.base_url = self._get_base_url(region)
    
    def _get_base_url(self, region):
        """Get base URL for the specified region."""
        endpoints = {
            "eu": "https://api-eu.securitycenter.microsoft.com",
            "eu3": "https://api-eu3.securitycenter.microsoft.com", 
            "us": "https://api.securitycenter.microsoft.com",
            "uk": "https://api-uk.securitycenter.microsoft.com"
        }
        return endpoints.get(region, endpoints["eu3"])
    
    def get_machine_by_dns_name(self, dns_name):
        """Get machine information by DNS name."""
        token = self._get_token()
        
        url = f"{self.base_url}/api/machines"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        params = {
            '$filter': f"computerDnsName eq '{dns_name}'",
            '$select': 'id'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise DefenderAPIError(f"Failed to query MS Defender API: {str(e)}")
    
    def get_machine_by_id(self, machine_id):
        """Get machine information by machine ID."""
        token = self._get_token()
        
        url = f"{self.base_url}/api/machines/{machine_id}"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise DefenderAPIError(f"Failed to query MS Defender API: {str(e)}")
    
    def get_machine_vulnerabilities(self, machine_id):
        """Get vulnerabilities for a machine."""
        token = self._get_token()
        
        url = f"{self.base_url}/api/machines/{machine_id}/vulnerabilities"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise DefenderAPIError(f"Failed to query MS Defender API: {str(e)}")
    
    def _get_token(self):
        """Get access token from authenticator."""
        scope = "https://graph.microsoft.com/.default"
        token = self.authenticator.get_token(scope)
        return token.token