"""
Tests for the connection service in the Affiliate Matrix backend.

This module contains tests for the ConnectionService class.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from ...services.connection_service import ConnectionService
from ...core.exceptions import ItemNotFoundError, ValidationError, ConnectionError, ExternalServiceError


@pytest.mark.asyncio
async def test_get_connections_list():
    """Test retrieving a paginated list of connections."""
    # Arrange
    connection_service = ConnectionService()
    
    # Act
    result = await connection_service.get_connections_list(
        page=1,
        limit=10
    )
    
    # Assert
    assert "data" in result
    assert "pagination" in result
    assert isinstance(result["data"], list)
    assert result["pagination"]["page"] == 1
    assert result["pagination"]["limit"] == 10
    assert result["pagination"]["total"] > 0
    assert result["pagination"]["total_pages"] > 0


@pytest.mark.asyncio
async def test_get_connections_list_with_filters():
    """Test retrieving a filtered list of connections."""
    # Arrange
    connection_service = ConnectionService()
    
    # Act
    result = await connection_service.get_connections_list(
        page=1,
        limit=10,
        type="api",
        status="connected"
    )
    
    # Assert
    assert "data" in result
    assert "pagination" in result
    assert isinstance(result["data"], list)
    # In a real test with a database, we would verify the filters were applied
    # For now, we just check that we got a valid response structure


@pytest.mark.asyncio
async def test_get_connection_by_id_existing():
    """Test retrieving an existing connection by ID."""
    # Arrange
    connection_service = ConnectionService()
    connection_id = "conn_1"  # This ID should exist in the mock data
    
    # Act
    connection = await connection_service.get_connection_by_id(connection_id)
    
    # Assert
    assert connection is not None
    assert connection["id"] == connection_id
    assert "name" in connection
    assert "status" in connection
    assert "type" in connection


@pytest.mark.asyncio
async def test_get_connection_by_id_not_found():
    """Test retrieving a non-existent connection by ID."""
    # Arrange
    connection_service = ConnectionService()
    connection_id = "non_existent_id"
    
    # Act & Assert
    with pytest.raises(ItemNotFoundError) as excinfo:
        await connection_service.get_connection_by_id(connection_id)
    
    assert "Connection not found" in str(excinfo.value)
    assert connection_id in str(excinfo.value)


@pytest.mark.asyncio
async def test_create_connection(mock_connection_data):
    """Test creating a new connection."""
    # Arrange
    connection_service = ConnectionService()
    connection_data = mock_connection_data
    
    # Remove the ID as it would be generated
    if "id" in connection_data:
        del connection_data["id"]
    
    # Act
    created_connection = await connection_service.create_connection(connection_data)
    
    # Assert
    assert created_connection is not None
    assert "id" in created_connection
    assert created_connection["name"] == connection_data["name"]
    assert created_connection["type"] == connection_data["type"]
    assert "createdAt" in created_connection
    assert "updatedAt" in created_connection


@pytest.mark.asyncio
async def test_update_connection(mock_connection_data):
    """Test updating an existing connection."""
    # Arrange
    connection_service = ConnectionService()
    connection_id = "conn_1"  # This ID should exist in the mock data
    
    update_data = {
        "name": "Updated Connection Name",
        "description": "Updated description",
        "settings": {
            "refreshInterval": 120,
            "autoSync": False
        }
    }
    
    # Act
    updated_connection = await connection_service.update_connection(connection_id, update_data)
    
    # Assert
    assert updated_connection is not None
    assert updated_connection["id"] == connection_id
    assert updated_connection["name"] == update_data["name"]
    assert updated_connection["description"] == update_data["description"]
    assert updated_connection["settings"]["refreshInterval"] == update_data["settings"]["refreshInterval"]
    assert updated_connection["settings"]["autoSync"] == update_data["settings"]["autoSync"]
    assert "updatedAt" in updated_connection


@pytest.mark.asyncio
async def test_update_connection_not_found():
    """Test updating a non-existent connection."""
    # Arrange
    connection_service = ConnectionService()
    connection_id = "non_existent_id"
    update_data = {"name": "Updated Name"}
    
    # Act & Assert
    with pytest.raises(ItemNotFoundError) as excinfo:
        await connection_service.update_connection(connection_id, update_data)
    
    assert "Connection not found" in str(excinfo.value)
    assert connection_id in str(excinfo.value)


@pytest.mark.asyncio
async def test_delete_connection():
    """Test deleting an existing connection."""
    # Arrange
    connection_service = ConnectionService()
    connection_id = "conn_1"  # This ID should exist in the mock data
    
    # Act
    await connection_service.delete_connection(connection_id)
    
    # Assert
    # In a real test with a database, we would verify the connection was deleted
    # For now, we just check that no exception was raised


@pytest.mark.asyncio
async def test_delete_connection_not_found():
    """Test deleting a non-existent connection."""
    # Arrange
    connection_service = ConnectionService()
    connection_id = "non_existent_id"
    
    # Act & Assert
    with pytest.raises(ItemNotFoundError) as excinfo:
        await connection_service.delete_connection(connection_id)
    
    assert "Connection not found" in str(excinfo.value)
    assert connection_id in str(excinfo.value)


@pytest.mark.asyncio
async def test_test_connection():
    """Test testing a connection."""
    # Arrange
    connection_service = ConnectionService()
    connection_id = "conn_1"  # This ID should exist in the mock data
    
    # Act
    status = await connection_service.test_connection(connection_id)
    
    # Assert
    assert status is not None
    assert "state" in status
    assert "lastChecked" in status
    assert "message" in status
    assert status["state"] in ["connected", "error"]


@pytest.mark.asyncio
async def test_test_connection_not_found():
    """Test testing a non-existent connection."""
    # Arrange
    connection_service = ConnectionService()
    connection_id = "non_existent_id"
    
    # Act & Assert
    with pytest.raises(ItemNotFoundError) as excinfo:
        await connection_service.test_connection(connection_id)
    
    assert "Connection not found" in str(excinfo.value)
    assert connection_id in str(excinfo.value)


@pytest.mark.asyncio
async def test_sync_connection():
    """Test syncing a connection."""
    # Arrange
    connection_service = ConnectionService()
    connection_id = "conn_1"  # This ID should exist in the mock data
    
    # Act
    updated_connection = await connection_service.sync_connection(connection_id)
    
    # Assert
    assert updated_connection is not None
    assert updated_connection["id"] == connection_id
    assert updated_connection["status"]["state"] == "syncing"
    assert updated_connection["status"]["syncProgress"] == 0
    assert "updatedAt" in updated_connection


@pytest.mark.asyncio
async def test_sync_connection_not_found():
    """Test syncing a non-existent connection."""
    # Arrange
    connection_service = ConnectionService()
    connection_id = "non_existent_id"
    
    # Act & Assert
    with pytest.raises(ItemNotFoundError) as excinfo:
        await connection_service.sync_connection(connection_id)
    
    assert "Connection not found" in str(excinfo.value)
    assert connection_id in str(excinfo.value)
