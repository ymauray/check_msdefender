# Detail Machine Feature

Get detailed machine information from Microsoft Defender.

## API Endpoint
- Base URL: `https://api.securitycenter.microsoft.com`
- Endpoint: `/api/machines/{machine_id}`
- Method: GET
- Authentication: Bearer token (Azure AD)

## Implementation

### Command Structure
```bash
check_msdefender detail -i <machine_id>
check_msdefender detail -d <dns_name> [-W <warning>] [-C <critical>]
```

### Service Class: `DetailService`
Location: `check_msdefender/services/detail_service.py`

**Methods:**
- `get_value(machine_id=None, dns_name=None)` - Returns machine details dict
- Inherits from base service pattern like `LastSeenService`

### CLI Command: `detail`
Location: `check_msdefender/cli/commands/detail.py`

**Pattern follows existing commands:**
- Uses `@common_options` decorator
- Creates `DefenderClient` and `DetailService`
- Uses `NagiosPlugin` for output formatting

### API Client Method
Location: `check_msdefender/core/defender.py`
- `get_machine_by_id(machine_id)` - Already implemented
- Returns full machine details JSON

## Output Format

### Success (Machine Found)
```
DEFENDER OK - Machine details retrieved | found=1;0;0
{
  "id": "89xxxxxxxxxxxxxx41f",
  "computerDnsName": "ma1.domain.tld",
  "lastSeen": "2024-01-15T10:30:00Z",
  "osPlatform": "Windows10",
  "version": "1909",
  "osProcessor": "x64",
  "lastIpAddress": "192.168.1.100",
  "lastExternalIpAddress": "203.0.113.1",
  "healthStatus": "Active",
  "deviceValue": "Normal",
  "rbacGroupId": 123,
  "riskScore": "Medium"
}
```

### Failure States
- **Warning**: `DEFENDER WARNING - Machine not found | found=0;0;1` (when warning=0)
- **Critical**: `DEFENDER CRITICAL - Machine not found | found=0;1;0` (when critical=0)
- **Unknown**: `DEFENDER UNKNOWN - API error: <message>` (API failures)

## Nagios Integration
- **OK**: Machine found and details retrieved
- **WARNING**: Machine not found when warning threshold = 0
- **CRITICAL**: Machine not found when critical threshold = 0
- **UNKNOWN**: API errors, authentication failures, network issues

## File Structure
```
check_msdefender/
├── cli/commands/detail.py          # CLI command implementation
├── services/detail_service.py      # Business logic service
└── core/defender.py               # API client (get_machine_by_id exists)
```

