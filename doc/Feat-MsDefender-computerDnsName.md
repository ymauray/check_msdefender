# Feature Specification: Machine ID Lookup by Computer DNS Name

## Overview
This feature enables the retrieval of machine IDs from Microsoft Defender for Endpoint by using the computer's DNS name (FQDN). This is essential for correlating machines across different monitoring systems and performing targeted security operations.

## Purpose
- Resolve machine DNS names to unique Microsoft Defender machine IDs
- Enable cross-referencing between DNS-based identification and Defender's internal machine tracking
- Support automated security workflows that start with DNS names but need machine IDs for Defender API operations

## Business Use Case
Security teams often have DNS names of machines from network monitoring tools, log files, or incident reports, but need the corresponding Microsoft Defender machine ID to:
- Query machine-specific security data
- Retrieve vulnerability information
- Check onboarding status
- Perform security actions

## API Requirements

### Authentication
- **Required**: Azure AD Application Registration with appropriate permissions
- **Scopes**: `WindowsDefenderATP` or `https://securitycenter.onmicrosoft.com/windowsdefenderatp/.default`
- **Permissions**: `Machine.Read.All` (minimum required)

### Geographic Endpoints
The Microsoft Defender for Endpoint API has different endpoints based on geographic location:
- **EU**: `https://api-eu.securitycenter.microsoft.com`
- **EU3**: `https://api-eu3.securitycenter.microsoft.com` (used in this example)
- **US**: `https://api.securitycenter.microsoft.com`
- **UK**: `https://api-uk.securitycenter.microsoft.com`

## API Implementation

### Endpoint
```
GET https://api-eu3.securitycenter.microsoft.com/api/machines
```

### Query Parameters
- **Filter by computerDnsName**: `$filter=computerDnsName eq 'fqdn'`
- **Select only the id**: `$select=id`

### Complete Query
```
https://api-eu3.securitycenter.microsoft.com/api/machines?$filter=computerDnsName eq 'fqdn'&$select=id
```

### Headers
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

### Expected Response
```json
{
  "@odata.context": "https://api-eu3.securitycenter.microsoft.com/api/$metadata#Machines(id)",
  "value": [
    {
      "id": "89xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1f"
    }
  ]
}
```

### Extracted Machine ID
```
89xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1f
```

## Implementation Details

### Modified Files
- **core/defender.py**: Added `get_machine_by_dns_name()` method to DefenderClient class for DNS name to machine ID resolution using Microsoft Graph API deviceManagement endpoint with deviceName filter.

### Migration Checklist: Microsoft Graph API to MS Defender API

**API Migration Tasks:**

1. ✅ **Change base_url from Microsoft Graph to MS Defender API endpoint**
   - From: `https://graph.microsoft.com/v1.0`
   - To: `https://api-eu3.securitycenter.microsoft.com` (or configurable geographic endpoint)

2. ✅ **Update get_machine_by_dns_name() method to use /api/machines endpoint**
   - From: `/deviceManagement/managedDevices`
   - To: `/api/machines`

3. ✅ **Change filter parameter from deviceName to computerDnsName**
   - From: `$filter=deviceName eq '{dns_name}'`
   - To: `$filter=computerDnsName eq '{dns_name}'`

4. ✅ **Update get_machine_by_id() method to use MS Defender machines endpoint**
   - From: `/deviceManagement/managedDevices/{machine_id}`
   - To: `/api/machines/{machine_id}`

5. ✅ **Fix get_machine_vulnerabilities() method endpoint path**
   - From: `/security/machines/{machine_id}/vulnerabilities`
   - To: `/api/machines/{machine_id}/vulnerabilities`

6. ✅ **Update authentication scope from Graph to WindowsDefenderATP**
   - From: `https://graph.microsoft.com/.default`
   - To: `https://securitycenter.onmicrosoft.com/windowsdefenderatp/.default`

7. ✅ **Add geographic endpoint configuration support**
   - Support EU, EU3, US, UK endpoints
   - Make base_url configurable in constructor

8. ✅ **Update error handling for MS Defender API responses**
   - Handle MS Defender-specific error responses
   - Update exception messages for context