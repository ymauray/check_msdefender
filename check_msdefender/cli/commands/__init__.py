"""Commands package for CLI."""

from .lastseen import lastseen
from .vulnerabilities import vulnerabilities
from .onboarding import onboarding

def register_all_commands(main_group):
    """Register all command groups with the main CLI group."""
    main_group.add_command(lastseen)
    main_group.add_command(vulnerabilities)
    main_group.add_command(onboarding)
