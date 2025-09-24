# Product Evidence Feature

Get product evidence details from Microsoft Defender for a specific asset and product.

## API Endpoint
- Base URL: `https://api.securitycenter.microsoft.com`
- Endpoint: `/api/mtp/tvm/analytics/productEvidence`
- Method: GET
- Authentication: Bearer token (Azure AD)

## Implementation

### Command Structure
```bash
check_msdefender productevidence -i <machine_id> <product_id> <product_version>
check_msdefender productevidence -d <dns_name> <product_id> <product_version>
```

### Service Class: `ProductEvidenceService`
Location: `check_msdefender/services/product_evidence_service.py`

**Methods:**
- `get_product_evidence(asset_id, product_id, product_version, non_cpe_program=False)` - Returns product evidence details
- Inherits from base service pattern like `LastSeenService`

### CLI Command: `product-evidence`
Location: `check_msdefender/cli/commands/product_evidence.py`

**Pattern follows existing commands:**
- Uses `@common_options` decorator
- Creates `DefenderClient` and `ProductEvidenceService`
- Uses `NagiosPlugin` for output formatting

### API Client Method
Location: `check_msdefender/core/defender.py`
- `get_product_evidence(asset_id, product_id, product_version, non_cpe_program=False)`
- Returns full product evidence details JSON

Example API call:
```
https://api.securitycenter.microsoft.com/apiproxy/mtp/tvm/analytics/productEvidence?assetId=xxxassetidxxx&productId=xxxproductidxxx&productVersion=xxxproductversionxxx&nonCpeProgram=false
```

**Sample Response:**
```json
{
  "diskPaths": [
    "C:\\Program Files\\Rocket Uniface 10 Community Edition\\common\\tomcat\\bin\\tomcat-juli.jar"
  ],
  "registryPaths": [],
  "lastSeenTimestampUtc": "2025-09-17 14:52:23"
}
```

## Output Format

### Success (Evidence Found)
```
DEFENDER OK - Product evidence found for asset | disk_paths=1;0;0 registry_paths=0;0;0
Disk paths: C:\Program Files\Rocket Uniface 10 Community Edition\common\tomcat\bin\tomcat-juli.jar
Last seen: 2025-09-17 14:52:23
```

### Failure States
- **Warning**: `DEFENDER WARNING - Product evidence incomplete | disk_paths=0;0;1 registry_paths=0;0;1`
- **Critical**: `DEFENDER CRITICAL - No product evidence found | disk_paths=0;1;0 registry_paths=0;1;0`
- **Unknown**: `DEFENDER UNKNOWN - API error: <message>` (API failures)

## Nagios Integration
- **OK**: Product evidence found with disk or registry paths
- **WARNING**: Incomplete evidence (missing expected paths)
- **CRITICAL**: No evidence found for the specified product
- **UNKNOWN**: API errors, authentication failures, network issues

## File Structure
```
check_msdefender/
├── cli/commands/product_evidence.py      # CLI command implementation
├── services/product_evidence_service.py  # Business logic service
└── core/defender.py                      # API client method
```

## Tests
- Unit tests
- Integration tests
- Fixture tests

## Validation
- black
- flake8
- mypy
- pytest