"""Detail service implementation."""

import json
from check_msdefender.core.exceptions import ValidationError
from check_msdefender.core.logging_config import get_verbose_logger


class DetailService:
    """Service for getting machine details."""

    def __init__(self, defender_client, verbose_level=0):
        """Initialize with Defender client."""
        self.defender = defender_client
        self.logger = get_verbose_logger(__name__, verbose_level)

    def get_value(self, machine_id=None, dns_name=None):
        """Get machine details.

        Returns:
            dict: Machine details, or count of found machines (1 or 0)
        """
        self.logger.method_entry("get_value", machine_id=machine_id, dns_name=dns_name)

        if not machine_id and not dns_name:
            raise ValidationError("Either machine_id or dns_name must be provided")

        try:
            # Get machine information
            if dns_name:
                self.logger.info(f"Fetching machine data by DNS name: {dns_name}")
                machines_data = self.defender.get_machine_by_dns_name(dns_name)
                if not machines_data.get('value'):
                    self.logger.info(f"Machine not found with DNS name: {dns_name}")
                    self.logger.method_exit("get_value", 0)
                    return 0  # Return 0 for not found (used for thresholds)
                machine_data = machines_data['value'][0]
                self.logger.debug(f"Found machine: {machine_data.get('id', 'unknown')}")
                machine_id = machine_data.get('id')

            # Get detailed machine information by ID
            self.logger.info(f"Fetching detailed machine data by ID: {machine_id}")
            machine_details = self.defender.get_machine_by_id(machine_id)

            # Store the details for output formatting
            self._machine_details = machine_details

            self.logger.info(f"Machine details retrieved successfully")
            self.logger.method_exit("get_value", 1)
            return 1  # Return 1 for found (used for thresholds)

        except Exception as e:
            self.logger.debug(f"Failed to get machine details: {str(e)}")
            raise

    def get_machine_details_json(self):
        """Get the machine details as formatted JSON string."""
        if not hasattr(self, '_machine_details'):
            return None
        return json.dumps(self._machine_details, indent=2)