# tests/core/test_key_management.py
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from backend.core.key_management import KeyManager

@pytest.fixture
def mock_vault():
    return Mock()

@pytest.fixture
def key_manager(mock_vault):
    return KeyManager(mock_vault)

def test_get_credential_success(key_manager, mock_vault):
    # Setup
    mock_vault.get_secret.return_value = "test-api-key"

    # Execute
    result = key_manager.get_credential("skimlinks", "api_key")

    # Verify
    assert result == "test-api-key"
    mock_vault.get_secret.assert_called_once_with(
        path="affiliate/skimlinks/api_key"
    )

def test_get_credential_caching(key_manager, mock_vault):
    # Setup
    mock_vault.get_secret.return_value = "test-api-key"

    # First call
    result1 = key_manager.get_credential("skimlinks", "api_key")

    # Second call should use cache
    result2 = key_manager.get_credential("skimlinks", "api_key")

    # Verify
    assert result1 == result2 == "test-api-key"
    mock_vault.get_secret.assert_called_once() # Should only call vault once

def test_get_credential_cache_expiry(key_manager, mock_vault):
    # Setup
    mock_vault.get_secret.return_value = "test-api-key"
    key_manager._cache_ttl = timedelta(seconds=0) # Immediate expiry

    # First call
    result1 = key_manager.get_credential("skimlinks", "api_key")

    # Second call should bypass cache due to expiry
    result2 = key_manager.get_credential("skimlinks", "api_key")

    # Verify
    assert result1 == result2 == "test-api-key"
    assert mock_vault.get_secret.call_count == 2

def test_store_credential_success(key_manager, mock_vault):
    # Execute
    result = key_manager.store_credential("skimlinks", "api_key", "new-api-key")

    # Verify
    assert result is True
    mock_vault.set_secret.assert_called_once_with(
        path="affiliate/skimlinks/api_key",
        value="new-api-key"
    )

def test_store_credential_invalidates_cache(key_manager, mock_vault):
    # Setup - populate cache
    mock_vault.get_secret.return_value = "old-api-key"
    key_manager.get_credential("skimlinks", "api_key")

    # Execute - store new value
    key_manager.store_credential("skimlinks", "api_key", "new-api-key")

    # Verify cache was invalidated
    mock_vault.get_secret.return_value = "new-api-key"
    result = key_manager.get_credential("skimlinks", "api_key")
    assert result == "new-api-key"

def test_delete_credential_success(key_manager, mock_vault):
    # Execute
    result = key_manager.delete_credential("skimlinks", "api_key")

    # Verify
    assert result is True
    mock_vault.delete_secret.assert_called_once_with(
        path="affiliate/skimlinks/api_key"
    )

def test_delete_credential_invalidates_cache(key_manager, mock_vault):
    # Setup - populate cache
    mock_vault.get_secret.return_value = "test-api-key"
    key_manager.get_credential("skimlinks", "api_key")

    # Execute - delete credential
    key_manager.delete_credential("skimlinks", "api_key")

    # Verify cache was invalidated
    mock_vault.get_secret.return_value = None
    result = key_manager.get_credential("skimlinks", "api_key")
    assert result is None
