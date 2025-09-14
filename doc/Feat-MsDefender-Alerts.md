# Alerts Machine Feature

Get detailed machine alerts from Microsoft Defender.

## API Endpoint
- Base URL: `https://api.securitycenter.microsoft.com`
- Endpoint: `/api/alerts`
- Method: GET
- Authentication: Bearer token (Azure AD)

## Implementation

### Command Structure
```bash
check_msdefender alerts -i <machine_id>
check_msdefender alerts -d <dns_name>
```

### Service Class: `AlertsService`
Location: `check_msdefender/services/alerts_service.py`

**Methods:**
- `get_alerts(machine_id=None, dns_name=None)` - Returns machine alerts
- Inherits from base service pattern like `LastSeenService`

### CLI Command: `alerts`
Location: `check_msdefender/cli/commands/alerts.py`

**Pattern follows existing commands:**
- Uses `@common_options` decorator
- Creates `DefenderClient` and `AlertsService`
- Uses `NagiosPlugin` for output formatting

### API Client Method
Location: `check_msdefender/core/defender.py`
- `get_alerts()`
- Returns full alerts details JSON

https://api.securitycenter.microsoft.com/api/alerts?$top=100&$expand=evidence&$orderby=alertCreationTime desc&$select=status,title,machineId,computerDnsName,alertCreationTime,firstEventTime,lastEventTime,lastUpdateTime

https://api.securitycenter.microsoft.com
/api/alerts
$top=100
$expand=evidence
$orderby=alertCreationTime desc
$select=status,title,machineId,computerDnsName,alertCreationTime,firstEventTime,lastEventTime,lastUpdateTime,severity

```json
{
  "@odata.context": "https://api-eu3.securitycenter.microsoft.com/api/$metadata#Alerts(status,title,machineId,computerDnsName,alertCreationTime,firstEventTime,lastEventTime,lastUpdateTime,severity)",
  "value": [
    {
      "severity": "Informational",
      "status": "New",
      "title": "Automated investigation started manually",
      "alertCreationTime": "2025-09-12T21:22:14.12Z",
      "firstEventTime": "2025-09-12T21:22:13.7175652Z",
      "lastEventTime": "2025-09-12T21:22:13.7175652Z",
      "lastUpdateTime": "2025-09-13T01:24:04.42Z",
      "machineId": "89xxxxxxxxxxxxxxxxxxxxxxx41f",
      "computerDnsName": "machine.domain.tld"
    },
    {
      "severity": "Informational",
      "status": "Resolved",
      "title": "Automated investigation started manually",
      "alertCreationTime": "2025-09-11T15:25:38.54Z",
      "firstEventTime": "2025-09-11T15:25:38.1183588Z",
      "lastEventTime": "2025-09-11T15:25:38.1183588Z",
      "lastUpdateTime": "2025-09-12T11:05:46.9966667Z",
      "machineId": "89xxxxxxxxxxxxxxxxxxxxxxx41f",
      "computerDnsName": "machine.domain.tld"
    }
  ]
}
```

## Output Format

### Success (Machine Found)
```
DEFENDER WARNING - Unresolved informational alerts for machine.domain.tld | alerts=3;0;0
2025-09-12T21:22:14.12Z - Automated investigation started manually (New informational)
alertCreationTime - Alert title (status severity)
alertCreationTime - Alert title (status severity)
```

### Failure States
- **Warning**: `DEFENDER WARNING - Unresolved informational alerts | alerts=0;0;1` 
- **Critical**: `DEFENDER CRITICAL - Unresolved alerts | alerts=0;1;0`
- **Unknown**: `DEFENDER UNKNOWN - API error: <message>` (API failures)

## Nagios Integration
- **OK**: No unresolved or alerts
- **WARNING**: Unresolved informational alerts 
- **CRITICAL**: Unresolved alerts
- **UNKNOWN**: API errors, authentication failures, network issues

## File Structure
```
check_msdefender/
├── cli/commands/alerts.py          # CLI command implementation
├── services/alerts_service.py      # Business logic service
└── core/defender.py               # API client (get_machine_by_id exists)
```

## Tests
- Test units
- Integration tests
- Fixture tests

## validation
- black
- flake8
- mypy
- pytest
