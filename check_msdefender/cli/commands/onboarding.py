"""Onboarding status commands for CLI."""

import click

from check_msdefender.core.auth import get_authenticator
from check_msdefender.core.config import load_config
from check_msdefender.core.defender import DefenderClient
from check_msdefender.core.nagios import NagiosPlugin
from check_msdefender.services.onboarding_service import OnboardingService
from ..decorators import common_options

@click.group()
def onboarding():
    """Check onboarding status for Microsoft Defender."""
    pass

@onboarding.command()
@common_options
@click.pass_context
def onboarding_cmd(config, verbose, machine_id, dns_name, warning, critical):
    """Check onboarding status for Microsoft Defender (alias for onboarding-status)."""
    warning = warning if warning is not None else 1
    critical = critical if critical is not None else 2

    try:
        # Load configuration
        cfg = load_config(config)

        # Get authenticator
        authenticator = get_authenticator(cfg)

        # Create Defender client
        client = DefenderClient(authenticator)

        # Create the appropriate service based on service
        service = OnboardingService(client)

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
