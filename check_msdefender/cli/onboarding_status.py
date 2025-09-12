"""Onboarding status CLI commands."""

import click
from check_msdefender.cli import execute_check


@click.command()
@click.option('-c', '--config', default='check_msdefender.ini', help='Configuration file path')
@click.option('-m', '--machine-id', help='Machine ID (GUID)')
@click.option('-d', '--dns-name', help='Computer DNS Name (FQDN)')
@click.option('-W', '--warning', type=float, default=1, help='Warning threshold (default: 1)')
@click.option('-C', '--critical', type=float, default=2, help='Critical threshold (default: 2)')
@click.option('-v', '--verbose', count=True, help='Increase verbosity')
def main(config, machine_id, dns_name, warning, critical, verbose):
    """Check onboarding status for Microsoft Defender."""
    click.echo("Warning: This command is deprecated. Use 'check_msdefender onboarding-status' instead.", err=True)
    return execute_check('onboardingStatus', machine_id, dns_name, warning, critical, config, verbose)