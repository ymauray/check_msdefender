"""Commands package for CLI."""

from .lastseen import register_lastseen_commands
from .vulnerabilities import register_vulnerability_commands
from .onboarding import register_onboarding_commands

def register_all_commands(main_group):
    """Register all commands with the main CLI group."""
    register_lastseen_commands(main_group)
    register_vulnerability_commands(main_group)
    register_onboarding_commands(main_group)
