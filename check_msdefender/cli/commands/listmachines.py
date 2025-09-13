"""List machines commands for CLI."""

import sys
import click

from check_msdefender.core.auth import get_authenticator
from check_msdefender.core.config import load_config
from check_msdefender.core.defender import DefenderClient
from check_msdefender.core.nagios import NagiosPlugin
from check_msdefender.services.listmachines_service import ListMachinesService
from ..decorators import common_options


def register_listmachines_commands(main_group):
    """Register list machines commands with the main CLI group."""

    @main_group.command('listmachines')
    @common_options
    def listmachines_cmd(config, verbose, machine_id, dns_name, warning, critical):
        """List all machines in Microsoft Defender for Endpoint."""
        warning = warning if warning is not None else 10
        critical = critical if critical is not None else 25

        try:
            # Load configuration
            cfg = load_config(config)

            # Get authenticator
            authenticator = get_authenticator(cfg)

            # Create Defender client
            client = DefenderClient(authenticator, verbose_level=verbose)

            # Create the service
            service = ListMachinesService(client, verbose_level=verbose)

            # Create Nagios plugin
            plugin = NagiosPlugin(service, 'listmachines')

            # Execute check
            result = plugin.check(
                warning=warning,
                critical=critical,
                verbose=verbose
            )

            sys.exit(result or 0)

        except Exception as e:
            print(f"UNKNOWN: {str(e)}")
            sys.exit(3)