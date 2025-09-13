# List machines

List machine in ms defender

https://api.securitycenter.microsoft.com/api/machines?$select=id,computerDnsName,version,exposureLevel,onboardingStatus,riskScore,isExcluded,lastSeen,healthStatus,isAadJoined,osPlatform

## Base Url
https://api.securitycenter.microsoft.com

## Url
/api/machines

## Select
$select=id,computerDnsName,onboardingStatus,osPlatform

## Cli

check_msdefender listmachines -W 10 -C 25 
DEFENDER OK - listmachines is 4 | listmachines=0;10;25
88xxxxxxxx01 ma1.domain.tld Onboarded Windows11
88xxxxxxxx02 ma2.domain.tld Onboarded Windows11
88xxxxxxxx03 ma3.domain.tld Onboarded Windows11
88xxxxxxxx04 ma4.domain.tld Onboarded Windows11

## Nagios

Ok if count < <warning>
Warning if count > <warning>
Critical if count > <critical>

