"""Integration tests for CLI interface end-to-end without external dependencies."""

import pytest
from unittest.mock import Mock, patch
from click.testing import CliRunner

from check_msdefender.cli import main


@pytest.fixture
def cli_runner():
    """Create CLI runner for testing."""
    return CliRunner()


class TestHelpCommand:
    """Test help command functionality."""

    def test_help_command(self, cli_runner):
        """Test help command displays usage information."""
        result = cli_runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "Check Microsoft Defender API endpoints and validate values." in result.output
        assert "Commands:" in result.output
        assert "lastseen" in result.output
        assert "onboarding" in result.output
        assert "vulnerabilities" in result.output

    def test_help_flag(self, cli_runner):
        """Test --help flag displays usage information."""
        result = cli_runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "Check Microsoft Defender API endpoints and validate values." in result.output


class TestLastSeenCommand:
    """Test lastseen command functionality."""

    @patch('check_msdefender.cli.commands.lastseen.load_config')
    @patch('check_msdefender.cli.commands.lastseen.get_authenticator')
    @patch('check_msdefender.cli.commands.lastseen.DefenderClient')
    @patch('check_msdefender.cli.commands.lastseen.LastSeenService')
    @patch('check_msdefender.cli.commands.lastseen.NagiosPlugin')
    def test_lastseen_without_args(self, mock_nagios, mock_service, mock_client, 
                                  mock_auth, mock_config, cli_runner):
        """Test lastseen command without arguments."""
        # Setup mocks
        mock_config.return_value = {'config': 'test'}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0
        
        result = cli_runner.invoke(main, ['lastseen'])
        
        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            machine_id=None,
            dns_name=None,
            warning=7,
            critical=30,
            verbose=0
        )

    @patch('check_msdefender.cli.commands.lastseen.load_config')
    @patch('check_msdefender.cli.commands.lastseen.get_authenticator')
    @patch('check_msdefender.cli.commands.lastseen.DefenderClient')
    @patch('check_msdefender.cli.commands.lastseen.LastSeenService')
    @patch('check_msdefender.cli.commands.lastseen.NagiosPlugin')
    def test_lastseen_with_dns_name(self, mock_nagios, mock_service, mock_client, 
                                   mock_auth, mock_config, cli_runner):
        """Test lastseen command with DNS name."""
        # Setup mocks
        mock_config.return_value = {'config': 'test'}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0
        
        result = cli_runner.invoke(main, ['lastseen', '-d', 'machine.domain.tld'])
        
        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            machine_id=None,
            dns_name='machine.domain.tld',
            warning=7,
            critical=30,
            verbose=0
        )

    @patch('check_msdefender.cli.commands.lastseen.load_config')
    def test_lastseen_command_error(self, mock_config, cli_runner):
        """Test lastseen command error handling."""
        mock_config.side_effect = Exception("Configuration error")
        
        result = cli_runner.invoke(main, ['lastseen', '-d', 'machine.domain.tld'])
        
        # Exit code should be 0 but output contains error
        assert result.exit_code == 0
        assert "UNKNOWN: Configuration error" in result.output


class TestOnboardingCommand:
    """Test onboarding command functionality."""

    @patch('check_msdefender.cli.commands.onboarding.load_config')
    @patch('check_msdefender.cli.commands.onboarding.get_authenticator')
    @patch('check_msdefender.cli.commands.onboarding.DefenderClient')
    @patch('check_msdefender.cli.commands.onboarding.OnboardingService')
    @patch('check_msdefender.cli.commands.onboarding.NagiosPlugin')
    def test_onboarding_with_dns_name(self, mock_nagios, mock_service, mock_client, 
                                     mock_auth, mock_config, cli_runner):
        """Test onboarding command with DNS name."""
        # Setup mocks
        mock_config.return_value = {'config': 'test'}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0
        
        result = cli_runner.invoke(main, ['onboarding', '-d', 'machine.domain.tld'])
        
        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            machine_id=None,
            dns_name='machine.domain.tld',
            warning=1,
            critical=2,
            verbose=0
        )

    @patch('check_msdefender.cli.commands.onboarding.load_config')
    def test_onboarding_command_error(self, mock_config, cli_runner):
        """Test onboarding command error handling."""
        mock_config.side_effect = Exception("Authentication failed")
        
        result = cli_runner.invoke(main, ['onboarding', '-d', 'machine.domain.tld'])
        
        assert result.exit_code == 0
        assert "UNKNOWN: Authentication failed" in result.output


class TestVulnerabilitiesCommand:
    """Test vulnerabilities command functionality."""

    @patch('check_msdefender.cli.commands.vulnerabilities.load_config')
    @patch('check_msdefender.cli.commands.vulnerabilities.get_authenticator')
    @patch('check_msdefender.cli.commands.vulnerabilities.DefenderClient')
    @patch('check_msdefender.cli.commands.vulnerabilities.VulnerabilitiesService')
    @patch('check_msdefender.cli.commands.vulnerabilities.NagiosPlugin')
    def test_vulnerabilities_with_dns_name(self, mock_nagios, mock_service, mock_client, 
                                          mock_auth, mock_config, cli_runner):
        """Test vulnerabilities command with DNS name."""
        # Setup mocks
        mock_config.return_value = {'config': 'test'}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0
        
        result = cli_runner.invoke(main, ['vulnerabilities', '-d', 'machine.domain.tld'])
        
        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            machine_id=None,
            dns_name='machine.domain.tld',
            warning=10,
            critical=100,
            verbose=0
        )

    @patch('check_msdefender.cli.commands.vulnerabilities.load_config')
    @patch('check_msdefender.cli.commands.vulnerabilities.get_authenticator')
    @patch('check_msdefender.cli.commands.vulnerabilities.DefenderClient')
    @patch('check_msdefender.cli.commands.vulnerabilities.VulnerabilitiesService')
    @patch('check_msdefender.cli.commands.vulnerabilities.NagiosPlugin')
    def test_vulnerabilities_with_verbose(self, mock_nagios, mock_service, mock_client, 
                                         mock_auth, mock_config, cli_runner):
        """Test vulnerabilities command with verbose flag."""
        # Setup mocks
        mock_config.return_value = {'config': 'test'}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0
        
        result = cli_runner.invoke(main, ['vulnerabilities', '-d', 'machine.domain.tld', '-v'])
        
        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            machine_id=None,
            dns_name='machine.domain.tld',
            warning=10,
            critical=100,
            verbose=1
        )

    @patch('check_msdefender.cli.commands.vulnerabilities.load_config')
    @patch('check_msdefender.cli.commands.vulnerabilities.get_authenticator')
    @patch('check_msdefender.cli.commands.vulnerabilities.DefenderClient')
    @patch('check_msdefender.cli.commands.vulnerabilities.VulnerabilitiesService')
    @patch('check_msdefender.cli.commands.vulnerabilities.NagiosPlugin')
    def test_vulnerabilities_with_multiple_verbose(self, mock_nagios, mock_service, mock_client, 
                                                  mock_auth, mock_config, cli_runner):
        """Test vulnerabilities command with multiple verbose flags."""
        # Setup mocks
        mock_config.return_value = {'config': 'test'}
        mock_auth.return_value = Mock()
        mock_client.return_value = Mock()
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_plugin = Mock()
        mock_nagios.return_value = mock_plugin
        mock_plugin.check.return_value = 0
        
        result = cli_runner.invoke(main, ['vulnerabilities', '-d', 'machine.domain.tld', '-vvvv'])
        
        assert result.exit_code == 0
        mock_plugin.check.assert_called_once_with(
            machine_id=None,
            dns_name='machine.domain.tld',
            warning=10,
            critical=100,
            verbose=4
        )

    @patch('check_msdefender.cli.commands.vulnerabilities.load_config')
    def test_vulnerabilities_command_error(self, mock_config, cli_runner):
        """Test vulnerabilities command error handling."""
        mock_config.side_effect = Exception("Service unavailable")
        
        result = cli_runner.invoke(main, ['vulnerabilities', '-d', 'machine.domain.tld'])
        
        assert result.exit_code == 0
        assert "UNKNOWN: Service unavailable" in result.output