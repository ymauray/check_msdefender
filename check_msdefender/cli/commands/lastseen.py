"""Last seen commands for CLI."""

import click

from check_msdefender.core.auth import get_authenticator
from check_msdefender.core.config import load_config
from check_msdefender.core.defender import DefenderClient
from check_msdefender.core.nagios import NagiosPlugin
from check_msdefender.services.lastseen_service import LastSeenService
from ..decorators import common_options

@click.group()
def lastseen():
    """Check last seen for Microsoft Defender."""
    pass

@lastseen.command()
@common_options
def lastseen_cmd(config, verbose, machine_id, dns_name, warning, critical):
    """Check days since last seen for Microsoft Defender."""
    warning = warning if warning is not None else 7
    critical = critical if critical is not None else 30

    try:
        # Load configuration
        cfg = load_config(config)

        # Get authenticator
        authenticator = get_authenticator(cfg)

        # Create Defender client
        client = DefenderClient(authenticator)

        # Create the appropriate service based on service
        service = LastSeenService(client)

        # Create Nagios plugin
        plugin = NagiosPlugin(service)

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