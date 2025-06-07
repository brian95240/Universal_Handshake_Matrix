"""
Test configuration for the Affiliate Matrix backend.

This module provides test fixtures and configuration for pytest.
"""

import os
import pytest
import asyncio
from typing import Dict, Any, Generator, AsyncGenerator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..app import app
from ..config import settings
from ..models.models import Base

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Override settings for testing
settings.DATABASE_URL = TEST_DATABASE_URL
settings.ENVIRONMENT = "test"
settings.ENABLE_FEATURE_FLAGS = True
settings.FEATURE_FLAGS = {
    "enable_delta_endpoints": True,
    "enable_vault_integration": False,
    "enable_advanced_filtering": True
}


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Create an instance of the default event loop for each test case.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """
    Create a test database engine.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_db(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session.
    """
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
def test_app(test_db) -> FastAPI:
    """
    Create a test FastAPI application.
    """
    # Override the get_db dependency
    async def override_get_db():
        yield test_db
    
    # Override dependencies
    app.dependency_overrides = {}
    
    return app


@pytest.fixture(scope="function")
def test_client(test_app) -> TestClient:
    """
    Create a test client for the FastAPI application.
    """
    with TestClient(test_app) as client:
        yield client


@pytest.fixture(scope="function")
def mock_program_data() -> Dict[str, Any]:
    """
    Create mock program data for testing.
    """
    return {
        "id": "prog_test1",
        "name": "Test Program",
        "url": "https://example.com/affiliate",
        "description": "A test affiliate program",
        "status": "active",
        "category": ["Technology", "E-commerce"],
        "tags": ["High Commission", "Fast Payout"],
        "commission": {
            "type": "percentage",
            "value": 10.5
        },
        "cookieDuration": 30,
        "epc": 1.25,
        "conversionRate": 2.5,
        "paymentMethods": ["PayPal", "Bank Transfer"],
        "paymentFrequency": "monthly",
        "minimumPayout": 50,
        "source": "Manual",
        "createdAt": "2023-01-01T00:00:00Z",
        "updatedAt": "2023-01-01T00:00:00Z"
    }


@pytest.fixture(scope="function")
def mock_connection_data() -> Dict[str, Any]:
    """
    Create mock connection data for testing.
    """
    return {
        "id": "conn_test1",
        "name": "Test Connection",
        "type": "api",
        "url": "https://example.com/api",
        "description": "A test connection",
        "status": {
            "state": "connected",
            "lastChecked": "2023-01-01T00:00:00Z",
            "message": "Connection is active"
        },
        "credentials": {
            "apiKey": "test_api_key",
            "apiSecret": "test_api_secret",
            "tokenExpiry": "2024-01-01T00:00:00Z"
        },
        "settings": {
            "refreshInterval": 60,
            "autoSync": True,
            "filters": {
                "categories": ["Technology"],
                "minCommission": 5.0
            }
        },
        "lastSync": "2023-01-01T00:00:00Z",
        "nextScheduledSync": "2023-01-02T00:00:00Z",
        "createdAt": "2023-01-01T00:00:00Z",
        "updatedAt": "2023-01-01T00:00:00Z"
    }
