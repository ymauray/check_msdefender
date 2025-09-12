"""Onboarding status commands for CLI."""

import click

from core.auth import get_authenticator
from core.config import load_config
from core.defender import DefenderClient
from core.nagios import NagiosPlugin
from services.onboarding_status_service import OnboardingStatusService
from ..decorators import common_options

@click.group()
def onboarding():
    """Check onboarding status for Microsoft Defender."""
    pass

@onboarding.command()
@common_options
@click.pass_context
def onboarding_cmd(ctx, config, verbose, machine_id, dns_name, warning, critical):
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
        service = OnboardingStatusService(client)

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
