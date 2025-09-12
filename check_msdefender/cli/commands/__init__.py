"""Commands package for CLI."""

from cli.commands.last_seen import last_seen

def register_all_commands(cli):
    """Register all command groups with the main CLI group."""
    cli.add_command(last_seen)
