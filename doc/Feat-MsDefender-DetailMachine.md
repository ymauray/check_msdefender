# List machines

Find a machine in defender

https://api.securitycenter.microsoft.com/api/machines/89xxxxxxxxxxxxxx41f

## Base Url
https://api.securitycenter.microsoft.com

## Url
/api/machines/89xxxxxxxxxxxxxx41f


## Cli

check_msdefender detail -i 89xxxxxxxxxxxxxx41f
check_msdefender detail -d ma1.domain.tld -W 0 -C 0

DEFENDER OK - detail is found | detail=1;0;0
{
    json output
}

## Nagios

Ok if found
Warning if notfound when <warning> == 0
Critical if notfound when <critical> == 0

