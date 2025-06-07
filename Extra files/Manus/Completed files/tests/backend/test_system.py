import pytest
from fastapi.testclient import TestClient
from ..app import app

client = TestClient(app)

class TestSystemAPI:
    """Test cases for the System API endpoints."""
    
    def test_get_system_metrics(self):
        """Test retrieving system metrics."""
        response = client.get("/api/system/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
        assert "cpu" in data
        assert "memory" in data
        assert "storage" in data
        assert "network" in data
        assert "index_stats" in data
        assert "api_stats" in data
    
    def test_get_system_metrics_with_period(self):
        """Test retrieving system metrics with a specific period."""
        response = client.get("/api/system/metrics", params={"period": "day"})
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
        assert "cpu" in data
        assert "memory" in data
        assert "storage" in data
        assert "network" in data
        assert "index_stats" in data
        assert "api_stats" in data
    
    def test_get_system_logs(self):
        """Test retrieving system logs."""
        response = client.get("/api/system/logs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_system_logs_with_filters(self):
        """Test retrieving system logs with filters."""
        response = client.get("/api/system/logs", params={
            "level": "info",
            "component": "api",
            "limit": 10
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10
    
    def test_get_system_status(self):
        """Test retrieving system status."""
        response = client.get("/api/system/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "components" in data
        assert "last_checked" in data
