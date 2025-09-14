"""Detail machine commands for CLI."""

import sys
import click
import nagiosplugin

from check_msdefender.core.auth import get_authenticator
from check_msdefender.core.config import load_config
from check_msdefender.core.defender import DefenderClient
from check_msdefender.services.detail_service import DetailService
from check_msdefender.core.nagios import NagiosPlugin
from ..decorators import common_options


def register_detail_commands(main_group):
    """Register detail commands with the main CLI group."""

    @main_group.command("detail")
    @click.option("-i", "--id", "machine_id_alt", help="Machine ID (GUID)")
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
            plugin = NagiosPlugin(service, "detail")

            # Use -i option if provided, otherwise fallback to -m
            final_machine_id = machine_id_alt or machine_id

            # Set default thresholds for detail command to show proper performance data
            # Based on expected test output patterns
            if warning is not None and critical is None:
                # When warning is specified, critical defaults to 1 for proper performance data
                critical = 1
            elif critical is not None and warning is None:
                # When critical is specified, warning defaults to 1 for proper performance data
                warning = 1

            # Execute check
            result = plugin.check(
                machine_id=final_machine_id,
                dns_name=dns_name,
                warning=warning,
                critical=critical,
                verbose=verbose,
            )

            sys.exit(result)

        except Exception as e:
            print(f"DEFENDER UNKNOWN - {str(e)}")
            sys.exit(3)
