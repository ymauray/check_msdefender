"""Vulnerabilities service implementation."""

from check_msdefender.services.models import VulnerabilityScore
from check_msdefender.core.exceptions import ValidationError


class VulnerabilitiesService:
    """Service for checking vulnerabilities."""
    
    def __init__(self, defender_client):
        """Initialize with Defender client."""
        self.client = defender_client
    
    def get_value(self, machine_id=None, dns_name=None):
        """Get vulnerability score for a machine."""
        if not machine_id and not dns_name:
            raise ValidationError("Either machine_id or dns_name must be provided")
        
        # Get machine ID if DNS name provided
        if dns_name:
            machines_data = self.client.get_machine_by_dns_name(dns_name)
            if not machines_data.get('value'):
                raise ValidationError(f"Machine not found with DNS name: {dns_name}")
            machine_id = machines_data['value'][0]['id']
        
        # Get vulnerabilities for the machine
        vulnerabilities_data = self.client.get_machine_vulnerabilities(machine_id)
        vulnerabilities = vulnerabilities_data.get('value', [])
        
        # Calculate vulnerability score
        score = VulnerabilityScore()
        
        for vuln in vulnerabilities:
            severity = vuln.get('severity', '').lower()
            if severity == 'critical':
                score.critical += 1
            elif severity == 'high':
                score.high += 1
            elif severity == 'medium':
                score.medium += 1
            elif severity == 'low':
                score.low += 1
        
        return score.total_score