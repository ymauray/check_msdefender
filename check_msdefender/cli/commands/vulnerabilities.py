"""Vulnerability commands for CLI."""

import click
from ..decorators import common_options
from ..core import execute_check


def register_vulnerability_commands(main_group):
    """Register vulnerability commands with the main CLI group."""
    
    @main_group.command('vulnerabilities')
    @common_options
    @click.pass_context
    def vulnerabilities_cmd(ctx, machine_id, dns_name, warning, critical):
        """Check vulnerability score for Microsoft Defender."""
        warning = warning if warning is not None else 10
        critical = critical if critical is not None else 100
        
        return execute_check('vulnerabilities', machine_id, dns_name, warning, critical, 
                            ctx.obj['config'], ctx.obj['verbose'])

    @main_group.command('vuln')
    @common_options
    @click.pass_context
    def vuln_cmd(ctx, machine_id, dns_name, warning, critical):
        """Check vulnerability score for Microsoft Defender (alias for vulnerabilities)."""
        warning = warning if warning is not None else 10
        critical = critical if critical is not None else 100
        
        return execute_check('vulnerabilities', machine_id, dns_name, warning, critical, 
                            ctx.obj['config'], ctx.obj['verbose'])

    @main_group.command('vulns')
    @common_options
    @click.pass_context
    def vulns_cmd(ctx, machine_id, dns_name, warning, critical):
        """Check vulnerability score for Microsoft Defender (short alias for vulnerabilities)."""
        warning = warning if warning is not None else 10
        critical = critical if critical is not None else 100
        
        return execute_check('vulnerabilities', machine_id, dns_name, warning, critical, 
                            ctx.obj['config'], ctx.obj['verbose'])