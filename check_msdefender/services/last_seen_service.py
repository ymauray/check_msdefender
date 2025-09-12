"""Last seen service implementation."""

from datetime import datetime
from check_msdefender.core.exceptions import ValidationError


class LastSeenService:
    """Service for checking last seen status."""
    
    def __init__(self, defender_client):
        """Initialize with Defender client."""
        self.client = defender_client
    
    def get_value(self, machine_id=None, dns_name=None):
        """Get days since last seen for a machine."""
        if not machine_id and not dns_name:
            raise ValidationError("Either machine_id or dns_name must be provided")
        
        # Get machine information
        if machine_id:
            machine_data = self.client.get_machine_by_id(machine_id)
        else:
            machines_data = self.client.get_machine_by_dns_name(dns_name)
            if not machines_data.get('value'):
                raise ValidationError(f"Machine not found with DNS name: {dns_name}")
            machine_data = machines_data['value'][0]
        
        # Extract last seen timestamp
        last_seen_str = machine_data.get('lastSeen')
        if not last_seen_str:
            raise ValidationError("No lastSeen data available for machine")
        
        # Parse timestamp and calculate days difference
        try:
            last_seen = datetime.fromisoformat(last_seen_str.replace('Z', '+00:00'))
            now = datetime.now(last_seen.tzinfo)
            days_diff = (now - last_seen).days
            return days_diff
        except (ValueError, TypeError) as e:
            raise ValidationError(f"Invalid lastSeen timestamp: {str(e)}")