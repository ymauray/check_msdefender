"""Vulnerabilities service implementation."""

from check_msdefender.services.models import VulnerabilityScore
from check_msdefender.core.exceptions import ValidationError
from check_msdefender.core.logging_config import get_verbose_logger


class VulnerabilitiesService:
    """Service for checking vulnerabilities."""
    
    def __init__(self, defender_client, verbose_level=0):
        """Initialize with Defender client."""
        self.client = defender_client
        self.logger = get_verbose_logger(__name__, verbose_level)
    
    def get_value(self, machine_id=None, dns_name=None):
        """Get vulnerability score for a machine."""
        self.logger.method_entry("get_value", machine_id=machine_id, dns_name=dns_name)
        
        if not machine_id and not dns_name:
            raise ValidationError("Either machine_id or dns_name must be provided")
        
        # Get machine ID if DNS name provided
        if dns_name:
            self.logger.info(f"Resolving machine ID for DNS name: {dns_name}")
            machines_data = self.client.get_machine_by_dns_name(dns_name)
            if not machines_data.get('value'):
                raise ValidationError(f"Machine not found with DNS name: {dns_name}")
            machine_id = machines_data['value'][0]['id']
            self.logger.debug(f"Resolved machine ID: {machine_id}")
        
        # Get vulnerabilities for the machine
        self.logger.info(f"Fetching vulnerabilities for machine: {machine_id}")
        vulnerabilities_data = self.client.get_machine_vulnerabilities(machine_id)
        vulnerabilities = vulnerabilities_data.get('value', [])
        self.logger.info(f"Found {len(vulnerabilities)} vulnerabilities")
        
        # Calculate vulnerability score
        score = VulnerabilityScore()
        
        for vuln in vulnerabilities:
            severity = vuln.get('severity', '').lower()
            vuln_id = vuln.get('id', 'unknown')
            self.logger.debug(f"Processing vulnerability {vuln_id} with severity: {severity}")
            
            if severity == 'critical':
                score.critical += 1
            elif severity == 'high':
                score.high += 1
            elif severity == 'medium':
                score.medium += 1
            elif severity == 'low':
                score.low += 1
        
        self.logger.info(f"Vulnerability score breakdown - Critical: {score.critical}, High: {score.high}, Medium: {score.medium}, Low: {score.low}")
        self.logger.info(f"Total vulnerability score: {score.total_score}")
        self.logger.method_exit("get_value", score.total_score)
        
        return score.total_score