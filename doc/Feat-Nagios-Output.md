# Nagios plugin

nagios plugin output is not precise enough.
Use DEFENDER instead of NAGIOSRESOURCE
Use command name instead of value

## Correct output
### lastseen
check_msdefender % check_msdefender lastseen -d machine.domain.tld
Actual : NAGIOSRESOURCE OK - value is 0 | value=0;7;30
Correct : DEFENDER OK - lastseen is 0 | value=0;7;30

### onboarding
check_msdefender onboarding -d machine.domain.tld
Actual : NAGIOSRESOURCE WARNING - value is 2 (outside range 0:1) | value=2;1;2
Correct : DEFENDER WARNING - onboarding is 2 (outside range 0:1) | value=2;1;2

### vulnerabilities
check_msdefender vulnerabilities -d machine.domain.tld    
DEFENDER CRITICAL - vulnerabilities is 294 (outside range 0:100) | value=294;10;100
