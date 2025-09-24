# Products Machine Feature

Get installed products and software from Microsoft Defender for a specific machine.

## API Endpoint
- Base URL: `https://api.securitycenter.windows.com`
- Endpoint: `/api/machines/SoftwareVulnerabilitiesByMachine`
- Method: GET
- Authentication: Bearer token (Azure AD)

## Implementation

### Command Structure
```bash
check_msdefender products -i <machine_id>
check_msdefender products -d <dns_name>
```

### Service Class: `ProductsService`
Location: `check_msdefender/services/products_service.py`

**Methods:**
- `get_products(machine_id=None, dns_name=None)` - Returns installed products for machine
- Inherits from base service pattern like `LastSeenService`

### CLI Command: `products`
Location: `check_msdefender/cli/commands/products.py`

**Pattern follows existing commands:**
- Uses `@common_options` decorator
- Creates `DefenderClient` and `ProductsService`
- Uses `NagiosPlugin` for output formatting

### API Client Method
Location: `check_msdefender/core/defender.py`
- `get_products(machine_id)`
- Returns full products details JSON

**Sample API Response:**
```json
{
  "@odata.context": "https://api-eu3.securitycenter.microsoft.com/api/$metadata#Collection(microsoft.windowsDefenderATP.api.AssetVulnerability)",
  "value": [
    {
      "id": "018d7dc428d98e16abed667a759f9e40a7e8f2c8_openssl_openssl_3.3.1.0_CVE-2024-9143",
      "deviceId": "018d7dc428d98e16abed667a759f9e40a7e8f2c8",
      "rbacGroupId": 0,
      "rbacGroupName": "Unassigned",
      "deviceName": "petit-tonnerre.arcantel.ch",
      "osPlatform": "Windows11",
      "osVersion": "10.0.26100.6584",
      "osArchitecture": "x64",
      "softwareVendor": "openssl",
      "softwareName": "openssl",
      "softwareVersion": "3.3.1.0",
      "cveId": "CVE-2024-9143",
      "vulnerabilitySeverityLevel": "Low",
      "recommendedSecurityUpdate": null,
      "recommendedSecurityUpdateId": null,
      "recommendedSecurityUpdateUrl": null,
      "diskPaths": [
        "c:\\program files\\druide\\antidote 12\\application\\bin64\\libcrypto-3-x64.dll",
        "c:\\program files\\druide\\antidote 12\\application\\bin64\\libssl-3-x64.dll",
        "c:\\program files\\druide\\connectix 12\\application\\bin64\\libcrypto-3-x64.dll",
        "c:\\program files\\druide\\connectix 12\\application\\bin64\\libssl-3-x64.dll"
      ],
      "registryPaths": [],
      "lastSeenTimestamp": "2025-09-17 14:52:23",
      "firstSeenTimestamp": "2025-09-10 11:18:18",
      "endOfSupportStatus": null,
      "endOfSupportDate": null,
      "exploitabilityLevel": "NoExploit",
      "recommendationReference": "va-_-openssl-_-openssl",
      "cvssScore": 3.7,
      "securityUpdateAvailable": true,
      "cveMitigationStatus": null
    },
```

## Output Format

### Success (Machine Found)
```
DEFENDER OK - 26 CVE found on machine.domain.tld | products=26;;;
openssl 3.3.1.0 (openssl) - 5 weaknesses (CVE-2024-9143, CVE-2024-9143..)
 - c:\\program files\\druide\\antidote 12\\application\\bin64\\libcrypto-3-x64.dll
 - c:\\program files\\druide\\antidote 12\\application\\bin64\\libssl-3-x64.dll
 - c:\\program files\\druide\\connectix 12\\application\\bin64\\libcrypto-3-x64.dll
 - c:\\program files\\druide\\connectix 12\\application\\bin64\\libssl-3-x64.dll
openssl 3.3.1.0 (openssl) - 5 weaknesses (CVE-2024-9143, CVE-2024-9143..)
 - c:\\program files\\druide\\antidote 12\\application\\bin64\\libcrypto-3-x64.dll
 - c:\\program files\\druide\\antidote 12\\application\\bin64\\libssl-3-x64.dll
 - c:\\program files\\druide\\connectix 12\\application\\bin64\\libcrypto-3-x64.dll
 - c:\\program files\\druide\\connectix 12\\application\\bin64\\libssl-3-x64.dll

```

### Failure States
- **Warning**: `DEFENDER WARNING - Products with vulnerabilities found | products=0;5;0`
- **Critical**: `DEFENDER CRITICAL - EOL products detected | products=0;0;3`
- **Unknown**: `DEFENDER UNKNOWN - API error: <message>` (API failures)

## Nagios Integration
- **OK**: Products found, no critical issues
- **WARNING**: Products with vulnerabilities detected
- **CRITICAL**: End-of-life (EOL) products detected
- **UNKNOWN**: API errors, authentication failures, network issues

## File Structure
```
check_msdefender/
├── cli/commands/products.py        # CLI command implementation
├── services/products_service.py    # Business logic service
└── core/defender.py               # API client (get_products method)
```

## Tests
- Test units
- Integration tests
- Fixture tests

## Validation
- black
- flake8
- mypy
- pytest