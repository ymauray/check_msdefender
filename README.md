# check_msdefender

A Nagios plugin for monitoring Microsoft Defender API endpoints and checking values.

## Features

- Simple cli interface
- Nagios plugin compatible output
- Query Microsoft Defender API endpoints
- Check and validate returned values against thresholds
- Support for Client Secret authentication
- Support for Client Certificate authentication
- Configuration file for authentication credentials
- Built using the nagiosplugin library
- Uses Microsoft Identity SDK for Python (azure-identity)

## Requirements

- Python 3.6+
- click
- nagiosplugin
- azure-identity

## Installation

### Method 1: Install from source (Recommended)

```bash
virtualenv /usr/local/libexec/nagios/check_msdefender
source /usr/local/libexec/nagios/check_msdefender/bin/activate.csh
pip install git+https://github.com/lduchosal/check_msdefender.git
```

For development installation:
```bash
pip install -e .
pip install -r requirements-dev.txt
```

### Post-Installation Setup

Create the default configuration file `check_msdefender.ini` in Nagios base directory (typically `/usr/local/etc/nagios`).

## Authentication

The plugin supports two authentication methods:

### Client Secret Authentication

Create a configuration file with your client credentials:

```ini
[auth]
client_id = your-client-id
client_secret = your-client-secret
tenant_id = your-tenant-id
```

### Client Certificate Authentication

For certificate-based authentication:

```ini
[auth]
client_id = your-client-id
tenant_id = your-tenant-id
certificate_path = /path/to/certificate.pem
private_key_path = /path/to/private_key.pem
```

## Usage

After installation via pip, you can use the plugin directly:

```bash
check_msdefender [options]
```

Or run it as a Python module:

```bash
python -m check_msdefender [options]
```

The plugin will automatically look for the configuration file `check_msdefender.ini` in the current directory or Nagios base directory. You can override this with the `-c` option:

```bash
check_msdefender -c /path/to/custom/config.ini [options]
```

### Command Line Options

- `-c, --config`: Configuration file path (optional, defaults to check_msdefender.ini in current or Nagios base directory)
- `-m, --machineId`: Machine Identified (GUID)
- `-d, --computerDnsName`:  Computer DNS Name (FQDN)
- `-W, --warning`: Warning threshold (numeric value)
- `-C, --critical`: Critical threshold (numeric value) 
- `-v, --verbose`: Increase verbosity (use -v, -vv, or -vvv)
- `-h, --help`: Show help message
- `--version`: Show version information
- Defender API endpoint (required)

### Examples

```bash
# Check onboardingStatus (using default config)
check_msdefender onboarding -d machine.domain.tld

# Check lastSeen
check_msdefender lastseen -d machine.domain.tld

# Check vulnerabilities
check_msdefender vulnerabilities -d machine.domain.tld
```


### Custom examples

```bash
# Check onboardingStatus (using  custom config)
check_msdefender onboarding -c /path/to/check_msdefender.ini -d "machine.domain.tld" -W 1 -C 2

# Check lastSeen, warning if > 1 week, critical if > 1 month
check_msdefender lastseen -d "machine.domain.tld" -W 7 -C 30

# Check vulnerabilities, critical if > 1 critical vulnerability, warning if > 1 high vulnerability
check_msdefender vulnerabilities -d "machine.domain.tld" -W 10 -C 100
```

### Supported Endpoints

- `onboarding`: Onboarded = (0), InsufficientInfo = (1), Unknown = (2)
- `lastseen`: Number of days since last seen (7)
- `vulnerabilities`: Sum of critical (*100) + high (*10) + medium (*5) + low (*1)

## Configuration File Format

```ini
[auth]
# Required for both authentication methods
client_id = your-application-client-id
tenant_id = your-azure-tenant-id

# For Client Secret authentication
client_secret = your-client-secret

# For Client Certificate authentication (alternative to client_secret)
certificate_path = /path/to/certificate.pem
private_key_path = /path/to/private_key.pem

[settings]
# Optional: Timeout in seconds (default: 5)
timeout = 5
```

## Nagios Configuration

### For pip-installed plugin:

Add the following to your Nagios commands configuration:

```cfg
#
# check_msdefender
#

# /usr/local/libexec/nagios/check_msdefender/bin/check_msdefender

define command {
    command_name    check_defender_vulnerabilities
    command_line    $USER1$/check_msdefender/bin/check_msdefender vulnerabilities -d $HOSTALIAS$ 
}

define command {
    command_name    check_defender_lastseen
    command_line    $USER1$/check_msdefender/bin/check_msdefender lastseen -d $HOSTALIAS$ 
}

define command {
    command_name    check_defender_onboarding
    command_line    $USER1$/check_msdefender/bin/check_msdefender onboarding -d $HOSTALIAS$ 
}
```

### Service definition examples:

```cfg
#
# svc-msdefender
#

define service {
    use                     generic-service
    service_description     DEFENDER_ONBOARDING
    check_command           check_defender_onboarding
    hostgroup_name          msdefender
}

define service {
    use                     generic-service
    service_description     DEFENDER_LASTSEEN
    check_command           check_defender_lastseen
    hostgroup_name          msdefender
}

define service {
    use                     generic-service
    service_description     DEFENDER_VULNERABILITIES
    check_command           check_defender_vulnerabilities
    hostgroup_name          msdefender
}
```

## Microsoft Defender API Setup

https://learn.microsoft.com/en-us/defender-endpoint/api/api-hello-world

1. Register an application in Azure Active Directory
2. Grant necessary Graph API permissions
3. Generate either a client secret or upload a certificate
4. Note down the client ID, tenant ID, and authentication credentials

Required API permissions (minimum):

WindowsDefenderATP (3)
Machine.Read.All
Vulnerability.Read
Vulnerability.Read.All

## Architecture

This plugin follows clean architecture principles:

### Package Structure

```
├── pyproject.toml                           # Modern Python packaging configuration
├── README.md                                # This documentation
├── LICENSE                                  # MIT License
├── check_msdefender.ini                     # Default configuration template
├── check_msdefender/                        # Python package
│   ├── __init__.py
│   ├── check_msdefender.py                  # Main entry point
│   ├── cli/
│   │   ├── onboarding_status.py
│   │   ├── last_seen.py
│   │   ├── vulnerabilities.py
│   │   ├── __init__.py
│   │   └── __main__.py                      # Support for `python -m check_msdefender`
│   ├── core/
│   │   ├── __init__.py
│   │   ├── nagios.py                        # NagiosPlugin implementation
│   │   ├── config.py                        # Configuration management
│   │   ├── auth.py                          # Authentication
│   │   ├── defender.py                      # Defender API client
│   │   └── exceptions.py                    # Custom exceptions
│   └── services/
│       ├── __init__.py
│       ├── onboarding_status_service.py     # onboarding_status implementation
│       ├── last_seen_service.py             # last_seen_service implementation
│       ├── vulnerabilities_service.py       # vulnerabilities implementation
│       └── models.py                        # Data models
└── tests/                                   # Test suite 
    ├── unit/
    ├── integration/
    └── fixtures/
```

Each component is:
- **Testable**: Clear interfaces and dependency injection
- **Extensible**: New authentication methods and validators can be added
- **Maintainable**: Separated concerns and minimal coupling

## Output

The plugin returns standard Nagios exit codes:
- 0 (OK): Value is within acceptable range
- 1 (WARNING): Value exceeds warning threshold
- 2 (CRITICAL): Value exceeds critical threshold  
- 3 (UNKNOWN): Error occurred during execution

## Development

### Setting up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/lduchosal/check_msdefender.git
cd check_msdefender
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
pip install -r requirements-dev.txt
```

### Building the Package

```bash
python -m build
```

This creates both wheel and source distributions in the `dist/` directory.

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black check_msdefender/

# Lint code  
flake8 check_msdefender/

# Type checking
mypy check_msdefender/
```

## Publishing to PyPI

### Test PyPI (for testing)

```bash
python -m twine upload --repository testpypi dist/*
```

### Production PyPI

```bash
python -m twine upload dist/*
```

## Troubleshooting

### Common Issues

- **Authentication Errors**: Ensure your Azure application has the required Graph API permissions
- **Configuration Issues**: Check that your authentication credentials are correct in the config file
- **Import Errors**: Make sure all dependencies are installed correctly
- **Network Connectivity**: Verify connectivity (firewall) to 
```
api-eu.securitycenter.microsoft.com
api-eu3.securitycenter.microsoft.com
api.securitycenter.microsoft.com
api-uk.securitycenter.microsoft.com

login.microsoftonline.com
```

### Debug Mode

Run with verbose output for troubleshooting:

```bash
check_msdefender vulnerabilities -vvvv
```

### Log Analysis

Review Nagios logs for detailed error messages:

```bash
tail -f /var/logs/nagios/nagios.log
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.