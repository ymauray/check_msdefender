"""Error handlers and formatters for click CLI."""

import click


class ClickErrorHandler:
    """Custom error handler for Click commands."""

    @staticmethod
    def handle_config_error(error):
        """Handle configuration-related errors."""
        click.echo(f"UNKNOWN: Configuration error - {str(error)}", err=True)
        return 3

    @staticmethod
    def handle_auth_error(error):
        """Handle authentication-related errors."""
        click.echo(f"UNKNOWN: Authentication error - {str(error)}", err=True)
        return 3

    @staticmethod
    def handle_api_error(error):
        """Handle API-related errors."""
        click.echo(f"UNKNOWN: API error - {str(error)}", err=True)
        return 3


class OutputFormatter:
    """Output formatters for different verbosity levels."""

    @staticmethod
    def format_verbose_output(message, verbose_level):
        """Format output based on verbosity level."""
        if verbose_level > 0:
            click.echo(f"DEBUG: {message}", err=True)

    @staticmethod
    def format_warning(message):
        """Format warning messages."""
        click.echo(f"WARNING: {message}", err=True)

    @staticmethod
    def format_error(message):
        """Format error messages."""
        click.echo(f"ERROR: {message}", err=True)
