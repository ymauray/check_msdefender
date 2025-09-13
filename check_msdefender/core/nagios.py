"""Nagios plugin implementation."""

import sys
import nagiosplugin
from nagiosplugin import Summary


class DefenderSummary(nagiosplugin.Summary):
    """Custom summary class for detailed Nagios output."""

    def __init__(self, details):
        """Initialize with detailed output lines."""
        self.details = details or []

    def ok(self, results):
        """Return detailed output for OK state."""
        return self._format_details()

    def problem(self, results):
        """Return detailed output for problem states (WARNING, CRITICAL)."""
        return self._format_details()

    def _format_details(self):
        """Format details for output."""
        if not self.details:
            return ''
        return '\n' + '\n'.join(self.details)


class NagiosPlugin:
    """Nagios plugin for Microsoft Defender monitoring."""

    def __init__(self, service, command_name):
        """Initialize with a service and command name."""
        self.service = service
        self.command_name = command_name
    
    def check(self, machine_id=None, dns_name=None, warning=None, critical=None, verbose=0):
        """Execute the check and return Nagios exit code."""
        try:
            result = self.service.get_result(
                machine_id=machine_id,
                dns_name=dns_name
            )
            value = result['value']
            details = result.get('details', [])

            # Create Nagios check with custom summary
            check = nagiosplugin.Check(
                DefenderResource(self.command_name, value),
                nagiosplugin.ScalarContext(self.command_name, warning, critical),
                DefenderSummary(details)
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

    def __init__(self, command_name, value):
        super().__init__()
        self.command_name = command_name
        self.value = value

    @property
    def name(self):
        """Return custom service name."""
        return 'DEFENDER'

    def probe(self):
        return [nagiosplugin.Metric(self.command_name, self.value)]