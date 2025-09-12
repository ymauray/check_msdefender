"""Legacy command for backward compatibility."""

import click
from ..core import execute_check


def register_legacy_commands():
    """Register legacy commands for backward compatibility."""
    
    @click.command()
    @click.option('-c', '--config', default='check_msdefender.ini', 
                  help='Configuration file path')
    @click.option('-m', '--machineId', help='Machine ID (GUID)')
    @click.option('-d', '--computerDnsName', help='Computer DNS Name (FQDN)')
    @click.option('-e', '--endpoint', required=True, 
                  help='Defender API endpoint')
    @click.option('-W', '--warning', type=float, help='Warning threshold')
    @click.option('-C', '--critical', type=float, help='Critical threshold')
    @click.option('-v', '--verbose', count=True, help='Increase verbosity')
    @click.version_option()
    def legacy_main(config, machineid, computerdnsname, endpoint, warning, critical, verbose):
        """Legacy command interface for backward compatibility."""
        click.echo("Warning: This command format is deprecated. Use the new subcommand format instead.", err=True)
        return execute_check(endpoint, machineid, computerdnsname, warning, critical, config, verbose)
    
    return legacy_main