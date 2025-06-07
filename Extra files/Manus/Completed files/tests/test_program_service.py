"""
Tests for the program service in the Affiliate Matrix backend.

This module contains tests for the ProgramService class.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from ...services.program_service import ProgramService
from ...core.exceptions import ItemNotFoundError, ValidationError


@pytest.mark.asyncio
async def test_get_programs_list():
    """Test retrieving a paginated list of programs."""
    # Arrange
    program_service = ProgramService()
    
    # Act
    result = await program_service.get_programs_list(
        page=1,
        limit=10,
        sort="name",
        order="asc"
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
async def test_get_programs_list_with_filters():
    """Test retrieving a filtered list of programs."""
    # Arrange
    program_service = ProgramService()
    
    # Act
    result = await program_service.get_programs_list(
        page=1,
        limit=10,
        status="active",
        category="Technology",
        min_commission=5.0
    )
    
    # Assert
    assert "data" in result
    assert "pagination" in result
    assert isinstance(result["data"], list)
    # In a real test with a database, we would verify the filters were applied
    # For now, we just check that we got a valid response structure


@pytest.mark.asyncio
async def test_get_program_by_id_existing():
    """Test retrieving an existing program by ID."""
    # Arrange
    program_service = ProgramService()
    program_id = "prog_1"  # This ID should exist in the mock data
    
    # Act
    program = await program_service.get_program_by_id(program_id)
    
    # Assert
    assert program is not None
    assert program["id"] == program_id
    assert "name" in program
    assert "status" in program


@pytest.mark.asyncio
async def test_get_program_by_id_not_found():
    """Test retrieving a non-existent program by ID."""
    # Arrange
    program_service = ProgramService()
    program_id = "non_existent_id"
    
    # Act & Assert
    with pytest.raises(ItemNotFoundError) as excinfo:
        await program_service.get_program_by_id(program_id)
    
    assert "Program not found" in str(excinfo.value)
    assert program_id in str(excinfo.value)


@pytest.mark.asyncio
async def test_create_program(mock_program_data):
    """Test creating a new program."""
    # Arrange
    program_service = ProgramService()
    program_data = mock_program_data
    
    # Remove the ID as it would be generated
    if "id" in program_data:
        del program_data["id"]
    
    # Act
    created_program = await program_service.create_program(program_data)
    
    # Assert
    assert created_program is not None
    assert "id" in created_program
    assert created_program["name"] == program_data["name"]
    assert created_program["status"] == program_data["status"]
    assert "createdAt" in created_program
    assert "updatedAt" in created_program


@pytest.mark.asyncio
async def test_update_program(mock_program_data):
    """Test updating an existing program."""
    # Arrange
    program_service = ProgramService()
    program_id = "prog_1"  # This ID should exist in the mock data
    
    update_data = {
        "name": "Updated Program Name",
        "status": "inactive",
        "description": "Updated description"
    }
    
    # Act
    updated_program = await program_service.update_program(program_id, update_data)
    
    # Assert
    assert updated_program is not None
    assert updated_program["id"] == program_id
    assert updated_program["name"] == update_data["name"]
    assert updated_program["status"] == update_data["status"]
    assert updated_program["description"] == update_data["description"]
    assert "updatedAt" in updated_program


@pytest.mark.asyncio
async def test_update_program_not_found():
    """Test updating a non-existent program."""
    # Arrange
    program_service = ProgramService()
    program_id = "non_existent_id"
    update_data = {"name": "Updated Name"}
    
    # Act & Assert
    with pytest.raises(ItemNotFoundError) as excinfo:
        await program_service.update_program(program_id, update_data)
    
    assert "Program not found" in str(excinfo.value)
    assert program_id in str(excinfo.value)


@pytest.mark.asyncio
async def test_delete_program():
    """Test deleting an existing program."""
    # Arrange
    program_service = ProgramService()
    program_id = "prog_1"  # This ID should exist in the mock data
    
    # Act
    await program_service.delete_program(program_id)
    
    # Assert
    # In a real test with a database, we would verify the program was deleted
    # For now, we just check that no exception was raised


@pytest.mark.asyncio
async def test_delete_program_not_found():
    """Test deleting a non-existent program."""
    # Arrange
    program_service = ProgramService()
    program_id = "non_existent_id"
    
    # Act & Assert
    with pytest.raises(ItemNotFoundError) as excinfo:
        await program_service.delete_program(program_id)
    
    assert "Program not found" in str(excinfo.value)
    assert program_id in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_program_metrics():
    """Test retrieving metrics for a program."""
    # Arrange
    program_service = ProgramService()
    program_id = "prog_1"  # This ID should exist in the mock data
    period = "month"
    
    # Act
    metrics = await program_service.get_program_metrics(program_id, period)
    
    # Assert
    assert metrics is not None
    assert "clicks" in metrics
    assert "impressions" in metrics
    assert "conversions" in metrics
    assert "revenue" in metrics
    assert "epc" in metrics
    assert "conversionRate" in metrics
