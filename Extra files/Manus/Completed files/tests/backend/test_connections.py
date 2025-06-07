import pytest
from fastapi.testclient import TestClient
from ..app import app

client = TestClient(app)

class TestConnectionsAPI:
    """Test cases for the Connections API endpoints."""
    
    def test_list_connections(self):
        """Test retrieving a paginated list of connections."""
        response = client.get("/api/connections")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert isinstance(data["data"], list)
    
    def test_list_connections_with_filters(self):
        """Test retrieving connections with filters."""
        response = client.get("/api/connections", params={
            "type": "api",
            "status": "connected"
        })
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
    
    def test_create_connection(self):
        """Test creating a new connection."""
        connection_data = {
            "name": "Test Connection",
            "type": "api",
            "url": "https://example.com/api",
            "description": "Test API connection",
            "credentials": {
                "api_key": "test_key"
            },
            "settings": {
                "refresh_interval": 60,
                "auto_sync": True
            }
        }
        response = client.post("/api/connections", json=connection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == connection_data["name"]
        assert "id" in data
        assert "status" in data
    
    def test_get_connection(self):
        """Test retrieving a specific connection."""
        # First create a connection
        connection_data = {
            "name": "Test Connection",
            "type": "api",
            "url": "https://example.com/api",
            "description": "Test API connection",
            "credentials": {
                "api_key": "test_key"
            },
            "settings": {
                "refresh_interval": 60,
                "auto_sync": True
            }
        }
        create_response = client.post("/api/connections", json=connection_data)
        connection_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/connections/{connection_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == connection_id
        assert data["name"] == connection_data["name"]
    
    def test_update_connection(self):
        """Test updating an existing connection."""
        # First create a connection
        connection_data = {
            "name": "Test Connection",
            "type": "api",
            "url": "https://example.com/api",
            "description": "Test API connection",
            "credentials": {
                "api_key": "test_key"
            },
            "settings": {
                "refresh_interval": 60,
                "auto_sync": True
            }
        }
        create_response = client.post("/api/connections", json=connection_data)
        connection_id = create_response.json()["id"]
        
        # Then update it
        update_data = {
            "name": "Updated Connection",
            "description": "Updated description"
        }
        response = client.put(f"/api/connections/{connection_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == connection_id
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
    
    def test_delete_connection(self):
        """Test deleting a connection."""
        # First create a connection
        connection_data = {
            "name": "Test Connection",
            "type": "api",
            "url": "https://example.com/api",
            "description": "Test API connection",
            "credentials": {
                "api_key": "test_key"
            },
            "settings": {
                "refresh_interval": 60,
                "auto_sync": True
            }
        }
        create_response = client.post("/api/connections", json=connection_data)
        connection_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(f"/api/connections/{connection_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/api/connections/{connection_id}")
        assert get_response.status_code == 404
    
    def test_sync_connection(self):
        """Test triggering synchronization for a connection."""
        # First create a connection
        connection_data = {
            "name": "Test Connection",
            "type": "api",
            "url": "https://example.com/api",
            "description": "Test API connection",
            "credentials": {
                "api_key": "test_key"
            },
            "settings": {
                "refresh_interval": 60,
                "auto_sync": True
            }
        }
        create_response = client.post("/api/connections", json=connection_data)
        connection_id = create_response.json()["id"]
        
        # Then sync it
        response = client.post(f"/api/connections/{connection_id}/sync")
        assert response.status_code == 202
        data = response.json()
        assert data["id"] == connection_id
        assert data["status"]["state"] == "syncing"
    
    def test_test_connection(self):
        """Test testing a connection."""
        # First create a connection
        connection_data = {
            "name": "Test Connection",
            "type": "api",
            "url": "https://example.com/api",
            "description": "Test API connection",
            "credentials": {
                "api_key": "test_key"
            },
            "settings": {
                "refresh_interval": 60,
                "auto_sync": True
            }
        }
        create_response = client.post("/api/connections", json=connection_data)
        connection_id = create_response.json()["id"]
        
        # Then test it
        response = client.post(f"/api/connections/{connection_id}/test")
        assert response.status_code == 200
        data = response.json()
        assert "state" in data
        assert "last_checked" in data
