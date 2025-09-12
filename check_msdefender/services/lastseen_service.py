"""Last seen service implementation."""

from datetime import datetime
from check_msdefender.core.exceptions import ValidationError
from check_msdefender.core.logging_config import get_verbose_logger


class LastSeenService:
    """Service for checking last seen status."""
    
    def __init__(self, defender_client, verbose_level=0):
        """Initialize with Defender client."""
        self.client = defender_client
        self.logger = get_verbose_logger(__name__, verbose_level)
    
    def get_value(self, machine_id=None, dns_name=None):
        """Get days since last seen for a machine."""
        self.logger.method_entry("get_value", machine_id=machine_id, dns_name=dns_name)
        
        if not machine_id and not dns_name:
            raise ValidationError("Either machine_id or dns_name must be provided")
        
        # Get machine information
        if machine_id:
            self.logger.info(f"Fetching machine data by ID: {machine_id}")
            machine_data = self.client.get_machine_by_id(machine_id)
        else:
            self.logger.info(f"Fetching machine data by DNS name: {dns_name}")
            machines_data = self.client.get_machine_by_dns_name(dns_name)
            if not machines_data.get('value'):
                raise ValidationError(f"Machine not found with DNS name: {dns_name}")
            machine_data = machines_data['value'][0]
            self.logger.debug(f"Found machine: {machine_data.get('id', 'unknown')}")
        
        # Extract last seen timestamp
        last_seen_str = machine_data.get('lastSeen')
        if not last_seen_str:
            raise ValidationError("No lastSeen data available for machine")
        
        self.logger.debug(f"Last seen timestamp from API: {last_seen_str}")
        
        # Parse timestamp and calculate days difference
        try:
            last_seen = datetime.fromisoformat(last_seen_str.replace('Z', '+00:00'))
            now = datetime.now(last_seen.tzinfo)
            days_diff = (now - last_seen).days
            
            self.logger.info(f"Machine last seen {days_diff} days ago ({last_seen_str})")
            self.logger.method_exit("get_value", days_diff)
            return days_diff
        except (ValueError, TypeError) as e:
            self.logger.debug(f"Failed to parse timestamp: {str(e)}")
            raise ValidationError(f"Invalid lastSeen timestamp: {str(e)}")