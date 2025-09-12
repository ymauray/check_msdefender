"""Last seen CLI commands."""

import click
from check_msdefender.cli import execute_check


@click.command()
@click.option('-c', '--config', default='check_msdefender.ini', help='Configuration file path')
@click.option('-m', '--machine-id', help='Machine ID (GUID)')
@click.option('-d', '--dns-name', help='Computer DNS Name (FQDN)')
@click.option('-W', '--warning', type=float, default=7, help='Warning threshold in days (default: 7)')
@click.option('-C', '--critical', type=float, default=30, help='Critical threshold in days (default: 30)')
@click.option('-v', '--verbose', count=True, help='Increase verbosity')
def main(config, machine_id, dns_name, warning, critical, verbose):
    """Check days since last seen for Microsoft Defender."""
    click.echo("Warning: This command is deprecated. Use 'check_msdefender last-seen' instead.", err=True)
    return execute_check('lastSeen', machine_id, dns_name, warning, critical, config, verbose)