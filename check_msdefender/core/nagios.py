"""Nagios plugin implementation."""

import nagiosplugin


class NagiosPlugin:
    """Nagios plugin for Microsoft Defender monitoring."""
    
    def __init__(self, service):
        """Initialize with a service."""
        self.service = service
    
    def check(self, machine_id=None, dns_name=None, warning=None, critical=None, verbose=0):
        """Execute the check and return Nagios exit code."""
        try:
            # Get value from service
            value = self.service.get_value(machine_id=machine_id, dns_name=dns_name)
            
            # Create Nagios check
            check = nagiosplugin.Check(
                NagiosResource(self.service, machine_id, dns_name),
                nagiosplugin.ScalarContext('value', warning, critical)
            )
            
            # Set verbosity
            check.verbosity = verbose
            
            # Run check
            check.main()
            
        except Exception as e:
            print(f"UNKNOWN: {str(e)}")
            return 3


class NagiosResource(nagiosplugin.Resource):
    """Nagios resource for getting values."""
    
    def __init__(self, service, machine_id, dns_name):
        self.service = service
        self.machine_id = machine_id
        self.dns_name = dns_name
    
    def probe(self):
        """Probe the resource and return metrics."""
        value = self.service.get_value(
            machine_id=self.machine_id,
            dns_name=self.dns_name
        )
        return [nagiosplugin.Metric('value', value)]