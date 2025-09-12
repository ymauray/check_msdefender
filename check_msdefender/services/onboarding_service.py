"""Onboarding status service implementation."""

from check_msdefender.services.models import OnboardingStatus
from check_msdefender.core.exceptions import ValidationError


class OnboardingService:
    """Service for checking onboarding status."""
    
    def __init__(self, defender_client):
        """Initialize with Defender client."""
        self.client = defender_client
    
    def get_value(self, machine_id=None, dns_name=None):
        """Get onboarding status value for a machine."""
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
        
        # Extract onboarding status
        # Note: This is a simplified implementation
        # Real implementation would parse the actual API response
        onboarding_state = machine_data.get('onboardingStatus', 'Unknown')
        
        if onboarding_state == 'Onboarded':
            return OnboardingStatus.ONBOARDED.value
        elif onboarding_state == 'InsufficientInfo':
            return OnboardingStatus.INSUFFICIENT_INFO.value
        else:
            return OnboardingStatus.UNKNOWN.value