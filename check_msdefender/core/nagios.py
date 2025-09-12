"""Nagios plugin implementation."""

import sys
import nagiosplugin


class NagiosPlugin:
    """Nagios plugin for Microsoft Defender monitoring."""
    
    def __init__(self, service, command_name):
        """Initialize with a service and command name."""
        self.service = service
        self.command_name = command_name
    
    def check(self, machine_id=None, dns_name=None, warning=None, critical=None, verbose=0):
        """Execute the check and return Nagios exit code."""
        try:
            # Get value from service
            value = self.service.get_value(machine_id=machine_id, dns_name=dns_name)
            
            # Create Nagios check
            check = nagiosplugin.Check(
                DefenderResource(self.service, machine_id, dns_name, self.command_name),
                nagiosplugin.ScalarContext(self.command_name, warning, critical)
            )
            
            # Set verbosity
            check.verbosity = verbose
            
            # Run check
            check.main()
            
        except Exception as e:
            print(f"UNKNOWN: {str(e)}")
            sys.exit(3)


class DefenderResource(nagiosplugin.Resource):
    """Defender resource for getting values with custom service name."""
    
    def __init__(self, service, machine_id, dns_name, command_name):
        super().__init__()
        self.service = service
        self.machine_id = machine_id
        self.dns_name = dns_name
        self.command_name = command_name
    
    @property 
    def name(self):
        """Return custom service name."""
        return 'DEFENDER'
    
    def probe(self):
        """Probe the resource and return metrics."""
        value = self.service.get_value(
            machine_id=self.machine_id,
            dns_name=self.dns_name
        )
        return [nagiosplugin.Metric(self.command_name, value)]