"""Commands package for CLI."""

from cli.commands.last_seen import last_seen
from cli.commands.vulnerabilities import vulnerabilities
from cli.commands.onboarding import onboarding_status

def register_all_commands(cli):
    """Register all command groups with the main CLI group."""
    cli.add_command(last_seen)
    cli.add_command(vulnerabilities)
    cli.add_command(onboarding_status)
