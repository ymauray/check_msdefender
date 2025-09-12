"""CLI module for check_msdefender."""

import click
from check_msdefender.core.config import load_config
from check_msdefender.core.auth import get_authenticator
from check_msdefender.core.defender import DefenderClient
from check_msdefender.core.nagios import NagiosPlugin
from check_msdefender.services.onboarding_status_service import OnboardingStatusService
from check_msdefender.services.last_seen_service import LastSeenService
from check_msdefender.services.vulnerabilities_service import VulnerabilitiesService


def common_options(func):
    """Decorator for common CLI options."""
    func = click.option('-m', '--machine-id', help='Machine ID (GUID)')(func)
    func = click.option('-d', '--dns-name', help='Computer DNS Name (FQDN)')(func)
    func = click.option('-W', '--warning', type=float, help='Warning threshold')(func)
    func = click.option('-C', '--critical', type=float, help='Critical threshold')(func)
    return func


@click.group()
@click.option('-c', '--config', default='check_msdefender.ini', 
              help='Configuration file path')
@click.option('-v', '--verbose', count=True, help='Increase verbosity')
@click.version_option()
@click.pass_context
def main(ctx, config, verbose):
    """Check Microsoft Defender API endpoints and validate values."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose


def execute_check(endpoint, machine_id, dns_name, warning, critical, config, verbose):
    """Execute a check for the specified endpoint."""
    try:
        # Load configuration
        cfg = load_config(config)
        
        # Get authenticator
        authenticator = get_authenticator(cfg)
        
        # Create Defender client
        client = DefenderClient(authenticator)
        
        # Create appropriate service based on endpoint
        if endpoint == 'onboardingStatus':
            service = OnboardingStatusService(client)
        elif endpoint == 'lastSeen':
            service = LastSeenService(client)
        elif endpoint == 'vulnerabilities':
            service = VulnerabilitiesService(client)
        else:
            raise ValueError(f"Unsupported endpoint: {endpoint}")
        
        # Create Nagios plugin
        plugin = NagiosPlugin(service)
        
        # Execute check
        result = plugin.check(
            machine_id=machine_id,
            dns_name=dns_name,
            warning=warning,
            critical=critical,
            verbose=verbose
        )
        
        return result
        
    except Exception as e:
        print(f"UNKNOWN: {str(e)}")
        return 3


@main.command('last-seen')
@common_options
@click.pass_context
def last_seen_cmd(ctx, machine_id, dns_name, warning, critical):
    """Check days since last seen for Microsoft Defender."""
    warning = warning if warning is not None else 7
    critical = critical if critical is not None else 30
    
    return execute_check('lastSeen', machine_id, dns_name, warning, critical, 
                        ctx.obj['config'], ctx.obj['verbose'])


@main.command('last')
@common_options
@click.pass_context
def last_cmd(ctx, machine_id, dns_name, warning, critical):
    """Check days since last seen for Microsoft Defender (alias for last-seen)."""
    warning = warning if warning is not None else 7
    critical = critical if critical is not None else 30
    
    return execute_check('lastSeen', machine_id, dns_name, warning, critical, 
                        ctx.obj['config'], ctx.obj['verbose'])


@main.command('ls')
@common_options
@click.pass_context
def ls_cmd(ctx, machine_id, dns_name, warning, critical):
    """Check days since last seen for Microsoft Defender (short alias for last-seen)."""
    warning = warning if warning is not None else 7
    critical = critical if critical is not None else 30
    
    return execute_check('lastSeen', machine_id, dns_name, warning, critical, 
                        ctx.obj['config'], ctx.obj['verbose'])


@main.command('onboarding-status')
@common_options
@click.pass_context
def onboarding_status_cmd(ctx, machine_id, dns_name, warning, critical):
    """Check onboarding status for Microsoft Defender."""
    warning = warning if warning is not None else 1
    critical = critical if critical is not None else 2
    
    return execute_check('onboardingStatus', machine_id, dns_name, warning, critical, 
                        ctx.obj['config'], ctx.obj['verbose'])


@main.command('onboarding')
@common_options
@click.pass_context
def onboarding_cmd(ctx, machine_id, dns_name, warning, critical):
    """Check onboarding status for Microsoft Defender (alias for onboarding-status)."""
    warning = warning if warning is not None else 1
    critical = critical if critical is not None else 2
    
    return execute_check('onboardingStatus', machine_id, dns_name, warning, critical, 
                        ctx.obj['config'], ctx.obj['verbose'])


@main.command('status')
@common_options
@click.pass_context
def status_cmd(ctx, machine_id, dns_name, warning, critical):
    """Check onboarding status for Microsoft Defender (short alias for onboarding-status)."""
    warning = warning if warning is not None else 1
    critical = critical if critical is not None else 2
    
    return execute_check('onboardingStatus', machine_id, dns_name, warning, critical, 
                        ctx.obj['config'], ctx.obj['verbose'])


@main.command('vulnerabilities')
@common_options
@click.pass_context
def vulnerabilities_cmd(ctx, machine_id, dns_name, warning, critical):
    """Check vulnerability score for Microsoft Defender."""
    warning = warning if warning is not None else 10
    critical = critical if critical is not None else 100
    
    return execute_check('vulnerabilities', machine_id, dns_name, warning, critical, 
                        ctx.obj['config'], ctx.obj['verbose'])


@main.command('vuln')
@common_options
@click.pass_context
def vuln_cmd(ctx, machine_id, dns_name, warning, critical):
    """Check vulnerability score for Microsoft Defender (alias for vulnerabilities)."""
    warning = warning if warning is not None else 10
    critical = critical if critical is not None else 100
    
    return execute_check('vulnerabilities', machine_id, dns_name, warning, critical, 
                        ctx.obj['config'], ctx.obj['verbose'])


@main.command('vulns')
@common_options
@click.pass_context
def vulns_cmd(ctx, machine_id, dns_name, warning, critical):
    """Check vulnerability score for Microsoft Defender (short alias for vulnerabilities)."""
    warning = warning if warning is not None else 10
    critical = critical if critical is not None else 100
    
    return execute_check('vulnerabilities', machine_id, dns_name, warning, critical, 
                        ctx.obj['config'], ctx.obj['verbose'])


# Backward compatibility: keep the legacy command structure for existing scripts
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