"""Fixture tests for LastSeenService."""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch

from check_msdefender.services.lastseen_service import LastSeenService
from check_msdefender.core.exceptions import ValidationError
from tests.fixtures.mock_defender_client import MockDefenderClient


class TestLastSeenServiceFixtures:
    """Fixture tests for LastSeenService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = MockDefenderClient()
        self.service = LastSeenService(self.mock_client)
    
    @patch('check_msdefender.services.lastseen_service.datetime')
    def test_get_value_by_machine_id(self, mock_datetime):
        """Test getting last seen value by machine ID."""
        # Mock current time to 2024-01-11T10:00:00Z for consistent results
        mock_now = datetime(2024, 1, 11, 10, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat
        
        # Test machine that was last seen 10 days ago (2024-01-01)
        result = self.service.get_value(machine_id="test-machine-1")
        assert result == 10
    
    @patch('check_msdefender.services.lastseen_service.datetime')
    def test_get_value_by_dns_name(self, mock_datetime):
        """Test getting last seen value by DNS name."""
        # Mock current time to 2024-01-11T10:00:00Z
        mock_now = datetime(2024, 1, 11, 10, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat
        
        # Test machine that was last seen 5 days ago (2024-01-05 to 2024-01-11 is 6 days but partial day = 5)
        result = self.service.get_value(dns_name="test-machine-2.domain.com")
        assert result == 5
    
    def test_get_value_no_parameters(self):
        """Test error when no parameters provided."""
        with pytest.raises(ValidationError, match="Either machine_id or dns_name must be provided"):
            self.service.get_value()
    
    def test_get_value_nonexistent_dns_name(self):
        """Test error when DNS name doesn't exist."""
        with pytest.raises(ValidationError, match="Machine not found with DNS name"):
            self.service.get_value(dns_name="nonexistent.domain.com")
    
    def test_get_value_nonexistent_machine_id(self):
        """Test error when machine ID doesn't exist.""" 
        with pytest.raises(ValidationError, match="Machine not found"):
            self.service.get_value(machine_id="nonexistent-machine")
    
    @patch('check_msdefender.services.lastseen_service.datetime')
    def test_get_value_machine_without_last_seen(self, mock_datetime):
        """Test error when machine has no lastSeen data."""
        # Create a mock client that returns machine without lastSeen
        class MockClientNoLastSeen:
            def get_machine_by_id(self, machine_id):
                return {"id": machine_id, "lastSeen": None}
        
        service = LastSeenService(MockClientNoLastSeen())
        
        with pytest.raises(ValidationError, match="No lastSeen data available"):
            service.get_value(machine_id="test-machine")
    
    def test_get_value_invalid_timestamp(self):
        """Test error when timestamp is invalid."""
        # Create a mock client that returns invalid timestamp
        class MockClientInvalidTimestamp:
            def get_machine_by_id(self, machine_id):
                return {"id": machine_id, "lastSeen": "invalid-timestamp"}
        
        service = LastSeenService(MockClientInvalidTimestamp())
        
        with pytest.raises(ValidationError, match="Invalid lastSeen timestamp"):
            service.get_value(machine_id="test-machine")
    
    def test_get_value_high_precision_microseconds_regression(self):
        """Test parsing timestamp with high precision microseconds - regression test."""
        import re
        
        # Create a mock client that returns timestamp with 7-digit microseconds
        class MockClientHighPrecision:
            def get_machine_by_id(self, machine_id):
                return {"id": machine_id, "lastSeen": "2025-09-12T13:14:52.3321473Z"}
        
        service = LastSeenService(MockClientHighPrecision())
        
        # Test that it works with the current implementation (might truncate microseconds)
        result = service.get_value(machine_id="test-machine")
        # Should return a reasonable value (depends on current time)
        assert isinstance(result, int)