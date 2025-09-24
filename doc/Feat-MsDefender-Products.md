# Products Machine Feature

Get installed products and software from Microsoft Defender for a specific machine.

## API Endpoint
- Base URL: `https://api.securitycenter.windows.com`
- Endpoint: `/api/tvm/analytics/assets/{machine_id}/installations/`
- Method: GET
- Authentication: Bearer token (Azure AD)
- Query Parameters: `?pageIndex=1&pageSize=100&$filter=(ProductCategory ne 'Component')&$orderby=isNormalized desc`

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
  "numOfResults": 26,
  "results": [
    {
      "installedVersion": "3.3.1.0",
      "tableIndicator": "SnapshotTable",
      "productNeverMatched": false,
      "productCategory": "Component",
      "installationId": "openssl-_-openssl-_-3.3.1.0",
      "productName": "openssl",
      "vendor": "openssl",
      "assetId": "xxx_machine_id_xxx",
      "assetName": "xxx_machine_name_xxx",
      "dnsName": "xxx_machine_dns_name_xxx",
      "firstSeen": "2025-09-10T09:59:49Z",
      "lastSeen": "2025-09-17T14:52:23Z",
      "weaknesses": 5,
      "threatInfo": {
        "hasExploit": false,
        "isExploitVerified": false,
        "isInExploitKit": false,
        "exploitTypes": [
          "Remote"
        ],
        "exploitUris": [],
        "isLinkedToThreat": false,
        "isThreatActive": false
      },
      "highSevAlert": false,
      "rawInfo": {
        "rawProgram": "The OpenSSL Toolkit",
        "rawVendor": "The OpenSSL Project, https://www.openssl.org/"
      },
      "rbacGroup": 0,
      "osName": "Windows11",
      "isNormalized": true,
      "eolSoftwareState": "NotEOL",
      "eolVersionState": "NotEOL",
      "eolVersionSinceDate": "2026-04-09T00:00:00+00:00",
      "osDistribution": "None",
      "totalUsageInDays": 0,
      "assetCriticalityLevel": 0,
      "assetCriticalityLevelText": "None",
      "tags": []
    }
  ]
}
```

## Output Format

### Success (Machine Found)
```
DEFENDER OK - 26 products installed on machine.domain.tld | products=26;;;
openssl 3.3.1.0 (openssl) - 5 weaknesses, EOL: 2026-04-09
installationId installedVersion (Vendor) - X weaknesses, EOL status
Product Version (Vendor) - X weaknesses, EOL status
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