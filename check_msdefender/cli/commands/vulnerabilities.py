"""Vulnerability commands for CLI."""

import click

from check_msdefender.core.auth import get_authenticator
from check_msdefender.core.config import load_config
from check_msdefender.core.defender import DefenderClient
from check_msdefender.core.nagios import NagiosPlugin
from check_msdefender.services.vulnerabilities_service import VulnerabilitiesService
from ..decorators import common_options


def register_vulnerability_commands(main_group):
    """Register vulnerability commands with the main CLI group."""
    
    @main_group.command('vulnerabilities')
    @common_options
    def vulnerabilities_cmd(config, verbose, machine_id, dns_name, warning, critical):
        """Check vulnerability score for Microsoft Defender."""
        warning = warning if warning is not None else 10
        critical = critical if critical is not None else 100

        try:
            # Load configuration
            cfg = load_config(config)

            # Get authenticator
            authenticator = get_authenticator(cfg)

            # Create Defender client
            client = DefenderClient(authenticator, verbose_level=verbose)

            # Create appropriate service based on endpoint
            service = VulnerabilitiesService(client, verbose_level=verbose)

            # Create Nagios plugin
            plugin = NagiosPlugin(service, 'vulnerabilities')

            # Execute check
            result = plugin.check(
                machine_id=machine_id,
                dns_name=dns_name,
                warning=warning,
                critical=critical,
                verbose=verbose
            )

            return result

        except Exception as e:
            print(f"UNKNOWN: {str(e)}")
            return 3
