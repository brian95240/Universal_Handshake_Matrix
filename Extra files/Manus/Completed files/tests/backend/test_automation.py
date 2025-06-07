import pytest
from fastapi.testclient import TestClient
from ..app import app

client = TestClient(app)

class TestAutomationAPI:
    """Test cases for the Automation API endpoints."""
    
    def test_list_triggers(self):
        """Test retrieving a paginated list of automation triggers."""
        response = client.get("/api/automation/triggers")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert isinstance(data["data"], list)
    
    def test_list_triggers_with_filters(self):
        """Test retrieving automation triggers with filters."""
        response = client.get("/api/automation/triggers", params={
            "type": "scheduled",
            "action": "discovery",
            "enabled": True
        })
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
    
    def test_create_trigger(self):
        """Test creating a new automation trigger."""
        trigger_data = {
            "name": "Daily Discovery",
            "type": "scheduled",
            "enabled": True,
            "action": "discovery",
            "schedule": {
                "frequency": "daily",
                "hour": 1,
                "minute": 0
            },
            "parameters": {
                "query": "affiliate program",
                "depth": 2
            }
        }
        response = client.post("/api/automation/triggers", json=trigger_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == trigger_data["name"]
        assert "id" in data
        assert data["enabled"] == trigger_data["enabled"]
    
    def test_get_trigger(self):
        """Test retrieving a specific automation trigger."""
        # First create a trigger
        trigger_data = {
            "name": "Daily Discovery",
            "type": "scheduled",
            "enabled": True,
            "action": "discovery",
            "schedule": {
                "frequency": "daily",
                "hour": 1,
                "minute": 0
            },
            "parameters": {
                "query": "affiliate program",
                "depth": 2
            }
        }
        create_response = client.post("/api/automation/triggers", json=trigger_data)
        trigger_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/automation/triggers/{trigger_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == trigger_id
        assert data["name"] == trigger_data["name"]
    
    def test_update_trigger(self):
        """Test updating an existing automation trigger."""
        # First create a trigger
        trigger_data = {
            "name": "Daily Discovery",
            "type": "scheduled",
            "enabled": True,
            "action": "discovery",
            "schedule": {
                "frequency": "daily",
                "hour": 1,
                "minute": 0
            },
            "parameters": {
                "query": "affiliate program",
                "depth": 2
            }
        }
        create_response = client.post("/api/automation/triggers", json=trigger_data)
        trigger_id = create_response.json()["id"]
        
        # Then update it
        update_data = {
            "name": "Updated Daily Discovery",
            "schedule": {
                "frequency": "daily",
                "hour": 2,
                "minute": 30
            }
        }
        response = client.put(f"/api/automation/triggers/{trigger_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == trigger_id
        assert data["name"] == update_data["name"]
        assert data["schedule"]["hour"] == update_data["schedule"]["hour"]
        assert data["schedule"]["minute"] == update_data["schedule"]["minute"]
    
    def test_delete_trigger(self):
        """Test deleting an automation trigger."""
        # First create a trigger
        trigger_data = {
            "name": "Daily Discovery",
            "type": "scheduled",
            "enabled": True,
            "action": "discovery",
            "schedule": {
                "frequency": "daily",
                "hour": 1,
                "minute": 0
            },
            "parameters": {
                "query": "affiliate program",
                "depth": 2
            }
        }
        create_response = client.post("/api/automation/triggers", json=trigger_data)
        trigger_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(f"/api/automation/triggers/{trigger_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/api/automation/triggers/{trigger_id}")
        assert get_response.status_code == 404
    
    def test_toggle_trigger(self):
        """Test toggling an automation trigger."""
        # First create a trigger
        trigger_data = {
            "name": "Daily Discovery",
            "type": "scheduled",
            "enabled": True,
            "action": "discovery",
            "schedule": {
                "frequency": "daily",
                "hour": 1,
                "minute": 0
            },
            "parameters": {
                "query": "affiliate program",
                "depth": 2
            }
        }
        create_response = client.post("/api/automation/triggers", json=trigger_data)
        trigger_id = create_response.json()["id"]
        
        # Then toggle it
        toggle_data = {
            "enabled": False
        }
        response = client.post(f"/api/automation/triggers/{trigger_id}/toggle", json=toggle_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == trigger_id
        assert data["enabled"] == toggle_data["enabled"]
    
    def test_execute_trigger(self):
        """Test manually executing an automation trigger."""
        # First create a trigger
        trigger_data = {
            "name": "Daily Discovery",
            "type": "scheduled",
            "enabled": True,
            "action": "discovery",
            "schedule": {
                "frequency": "daily",
                "hour": 1,
                "minute": 0
            },
            "parameters": {
                "query": "affiliate program",
                "depth": 2
            }
        }
        create_response = client.post("/api/automation/triggers", json=trigger_data)
        trigger_id = create_response.json()["id"]
        
        # Then execute it
        response = client.post(f"/api/automation/triggers/{trigger_id}/execute")
        assert response.status_code == 202
        data = response.json()
        assert "status" in data
        assert data["status"] == "initiated"
