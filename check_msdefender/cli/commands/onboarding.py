"""Onboarding status commands for CLI."""

import click
from ..decorators import common_options
from ..core import execute_check


def register_onboarding_commands(main_group):
    """Register onboarding status commands with the main CLI group."""
    
    @main_group.command('onboarding-status')
    @common_options
    @click.pass_context
    def onboarding_status_cmd(ctx, machine_id, dns_name, warning, critical):
        """Check onboarding status for Microsoft Defender."""
        warning = warning if warning is not None else 1
        critical = critical if critical is not None else 2
        
        return execute_check('onboardingStatus', machine_id, dns_name, warning, critical, 
                            ctx.obj['config'], ctx.obj['verbose'])

    @main_group.command('onboarding')
    @common_options
    @click.pass_context
    def onboarding_cmd(ctx, machine_id, dns_name, warning, critical):
        """Check onboarding status for Microsoft Defender (alias for onboarding-status)."""
        warning = warning if warning is not None else 1
        critical = critical if critical is not None else 2
        
        return execute_check('onboardingStatus', machine_id, dns_name, warning, critical, 
                            ctx.obj['config'], ctx.obj['verbose'])

    @main_group.command('status')
    @common_options
    @click.pass_context
    def status_cmd(ctx, machine_id, dns_name, warning, critical):
        """Check onboarding status for Microsoft Defender (short alias for onboarding-status)."""
        warning = warning if warning is not None else 1
        critical = critical if critical is not None else 2
        
        return execute_check('onboardingStatus', machine_id, dns_name, warning, critical, 
                            ctx.obj['config'], ctx.obj['verbose'])