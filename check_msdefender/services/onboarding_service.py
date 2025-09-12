"""Onboarding status service implementation."""

from check_msdefender.services.models import OnboardingStatus
from check_msdefender.core.exceptions import ValidationError
from check_msdefender.core.logging_config import get_verbose_logger


class OnboardingService:
    """Service for checking onboarding status."""
    
    def __init__(self, defender_client, verbose_level=0):
        """Initialize with Defender client."""
        self.defender = defender_client
        self.logger = get_verbose_logger(__name__, verbose_level)
    
    def get_value(self, machine_id=None, dns_name=None):
        """Get onboarding status value for a machine."""
        self.logger.method_entry("get_value", machine_id=machine_id, dns_name=dns_name)
        
        if not machine_id and not dns_name:
            raise ValidationError("Either machine_id or dns_name must be provided")
        
        # Get machine information
        if dns_name:
            self.logger.info(f"Fetching machine data by DNS name: {dns_name}")
            machines_data = self.defender.get_machine_by_dns_name(dns_name)
            if not machines_data.get('value'):
                raise ValidationError(f"Machine not found with DNS name: {dns_name}")
            machine_data = machines_data['value'][0]
            self.logger.debug(f"Found machine: {machine_data.get('id', 'unknown')}")
            machine_id = machine_data.get('id')

        # Extract last seen timestamp
        onboarding_state = self.defender.get_machine_by_id(machine_id)['onboardingStatus']
        self.logger.debug(f"Raw onboarding status from API: {onboarding_state}")
        
        if onboarding_state == 'Onboarded':
            result = OnboardingStatus.ONBOARDED.value
        elif onboarding_state == 'InsufficientInfo':
            result = OnboardingStatus.INSUFFICIENT_INFO.value
        else:
            result = OnboardingStatus.UNKNOWN.value
        
        self.logger.info(f"Machine onboarding status: {onboarding_state} -> {result}")
        self.logger.method_exit("get_value", result)
        return result