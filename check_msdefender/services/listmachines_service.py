"""List machines service implementation."""

from check_msdefender.core.exceptions import ValidationError
from check_msdefender.core.logging_config import get_verbose_logger


class ListMachinesService:
    """Service for listing machines."""

    def __init__(self, defender_client, verbose_level=0):
        """Initialize with Defender client."""
        self.defender = defender_client
        self.logger = get_verbose_logger(__name__, verbose_level)

    def get_value(self, **kwargs):
        """Get count of machines."""
        self.logger.method_entry("get_value")

        # Get all machines
        self.logger.info("Fetching all machines from Defender API")
        machines_data = self.defender.list_machines()

        if not machines_data.get('value'):
            self.logger.info("No machines found")
            self.logger.method_exit("get_value", 0)
            return 0

        machines = machines_data['value']
        machine_count = len(machines)

        self.logger.info(f"Found {machine_count} machines")
        self.logger.method_exit("get_value", machine_count)
        return machine_count

    def get_details(self, **kwargs):
        """Get detailed machine information."""
        self.logger.method_entry("get_details")

        # Get all machines
        self.logger.info("Fetching all machines from Defender API")
        machines_data = self.defender.list_machines()

        if not machines_data.get('value'):
            self.logger.info("No machines found")
            self.logger.method_exit("get_details", [])
            return []

        machines = machines_data['value']
        details = []

        for machine in machines:
            machine_id = machine.get('id', 'unknown')[:10]  # Truncate ID for display
            dns_name = machine.get('computerDnsName', 'unknown')
            status = machine.get('onboardingStatus', 'unknown')
            platform = machine.get('osPlatform', 'unknown')

            details.append(f"{machine_id} {dns_name} {status} {platform}")

        self.logger.info(f"Prepared details for {len(details)} machines")
        self.logger.method_exit("get_details", details)
        return details