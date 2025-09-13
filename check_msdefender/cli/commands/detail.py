"""Detail machine commands for CLI."""

import sys
import click
import nagiosplugin

from check_msdefender.core.auth import get_authenticator
from check_msdefender.core.config import load_config
from check_msdefender.core.defender import DefenderClient
from check_msdefender.services.detail_service import DetailService
from ..decorators import common_options


class DetailNagiosPlugin:
    """Custom Nagios plugin for detail command with JSON output."""

    def __init__(self, service, command_name):
        """Initialize with a service and command name."""
        self.service = service
        self.command_name = command_name

    def check(self, machine_id=None, dns_name=None, warning=None, critical=None, verbose=0):
        """Execute the check and return Nagios exit code."""
        try:
            # Get value from service (returns 1 if found, 0 if not found)
            found = self.service.get_value(machine_id=machine_id, dns_name=dns_name)

            if found:
                # Machine found - output details
                details_json = self.service.get_machine_details_json()
                print(f"DEFENDER OK - Machine details retrieved | found=1;0;0")
                if details_json:
                    print(details_json)
                return 0
            else:
                # Machine not found - check thresholds
                if warning is not None and found <= warning:
                    print(f"DEFENDER WARNING - Machine not found | found=0;0;1")
                    return 1
                elif critical is not None and found <= critical:
                    print(f"DEFENDER CRITICAL - Machine not found | found=0;1;0")
                    return 2
                else:
                    # Default: not found is OK if no thresholds set
                    print(f"DEFENDER OK - Machine not found | found=0;0;0")
                    return 0

        except Exception as e:
            print(f"DEFENDER UNKNOWN - API error: {str(e)}")
            return 3


def register_detail_commands(main_group):
    """Register detail commands with the main CLI group."""

    @main_group.command('detail')
    @click.option('-i', '--id', 'machine_id_alt', help='Machine ID (GUID)')
    @common_options
    def detail_cmd(config, verbose, machine_id, dns_name, warning, critical, machine_id_alt):
        """Get detailed machine information from Microsoft Defender."""
        try:
            # Load configuration
            cfg = load_config(config)

            # Get authenticator
            authenticator = get_authenticator(cfg)

            # Create Defender client
            client = DefenderClient(authenticator, verbose_level=verbose)

            # Create the detail service
            service = DetailService(client, verbose_level=verbose)

            # Create custom Nagios plugin for detail output
            plugin = DetailNagiosPlugin(service, 'detail')

            # Use -i option if provided, otherwise fallback to -m
            final_machine_id = machine_id_alt or machine_id

            # Execute check
            result = plugin.check(
                machine_id=final_machine_id,
                dns_name=dns_name,
                warning=warning,
                critical=critical,
                verbose=verbose
            )

            sys.exit(result)

        except Exception as e:
            print(f"DEFENDER UNKNOWN - {str(e)}")
            sys.exit(3)