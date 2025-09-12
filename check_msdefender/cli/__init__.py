"""CLI module for check_msdefender."""

import click
from .commands import register_all_commands


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx, config, verbose):
    """Check Microsoft Defender API endpoints and validate values."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose


# Register all commands
register_all_commands(cli)