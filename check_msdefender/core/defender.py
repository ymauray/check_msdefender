"""Microsoft Defender API client."""

import requests
from check_msdefender.core.exceptions import DefenderAPIError


class DefenderClient:
    """Client for Microsoft Defender API."""
    
    def __init__(self, authenticator, timeout=5):
        """Initialize with authenticator."""
        self.authenticator = authenticator
        self.timeout = timeout
        self.base_url = "https://graph.microsoft.com/v1.0"
    
    def get_machine_by_dns_name(self, dns_name):
        """Get machine information by DNS name."""
        token = self._get_token()
        
        url = f"{self.base_url}/deviceManagement/managedDevices"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        params = {
            '$filter': f"deviceName eq '{dns_name}'"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise DefenderAPIError(f"Failed to query Defender API: {str(e)}")
    
    def get_machine_by_id(self, machine_id):
        """Get machine information by machine ID."""
        token = self._get_token()
        
        url = f"{self.base_url}/deviceManagement/managedDevices/{machine_id}"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise DefenderAPIError(f"Failed to query Defender API: {str(e)}")
    
    def get_machine_vulnerabilities(self, machine_id):
        """Get vulnerabilities for a machine."""
        token = self._get_token()
        
        url = f"{self.base_url}/security/machines/{machine_id}/vulnerabilities"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise DefenderAPIError(f"Failed to query Defender API: {str(e)}")
    
    def _get_token(self):
        """Get access token from authenticator."""
        scope = "https://graph.microsoft.com/.default"
        token = self.authenticator.get_token(scope)
        return token.token