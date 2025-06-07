import pytest
from fastapi.testclient import TestClient
from ..app import app

client = TestClient(app)

class TestDiscoveryAPI:
    """Test cases for the Discovery API endpoints."""
    
    def test_list_discovery_results(self):
        """Test retrieving a paginated list of discovery results."""
        response = client.get("/api/discovery")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert isinstance(data["data"], list)
    
    def test_list_discovery_results_with_filters(self):
        """Test retrieving discovery results with filters."""
        response = client.get("/api/discovery", params={
            "status": "completed",
            "startDate": "2025-01-01T00:00:00Z",
            "endDate": "2025-12-31T23:59:59Z"
        })
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
    
    def test_start_discovery(self):
        """Test starting a new discovery operation."""
        discovery_data = {
            "query": "affiliate program",
            "parameters": {
                "depth": 2,
                "max_results": 50
            }
        }
        response = client.post("/api/discovery", json=discovery_data)
        assert response.status_code == 202
        data = response.json()
        assert data["query"] == discovery_data["query"]
        assert "id" in data
        assert data["status"] == "in_progress"
    
    def test_get_discovery_result(self):
        """Test retrieving a specific discovery result."""
        # First start a discovery
        discovery_data = {
            "query": "affiliate program",
            "parameters": {
                "depth": 2,
                "max_results": 50
            }
        }
        create_response = client.post("/api/discovery", json=discovery_data)
        discovery_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/discovery/{discovery_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == discovery_id
        assert data["query"] == discovery_data["query"]
    
    def test_cancel_discovery(self):
        """Test cancelling an in-progress discovery operation."""
        # First start a discovery
        discovery_data = {
            "query": "affiliate program",
            "parameters": {
                "depth": 2,
                "max_results": 50
            }
        }
        create_response = client.post("/api/discovery", json=discovery_data)
        discovery_id = create_response.json()["id"]
        
        # Then cancel it
        response = client.post(f"/api/discovery/{discovery_id}/cancel")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == discovery_id
        assert "error" in data
    
    def test_process_discovery_item(self):
        """Test processing a discovery item."""
        # First start a discovery
        discovery_data = {
            "query": "affiliate program",
            "parameters": {
                "depth": 2,
                "max_results": 50
            }
        }
        create_response = client.post("/api/discovery", json=discovery_data)
        discovery_id = create_response.json()["id"]
        
        # Get the discovery result to find an item
        get_response = client.get(f"/api/discovery/{discovery_id}")
        if len(get_response.json()["results"]) > 0:
            item_id = get_response.json()["results"][0]["id"]
            
            # Process the item
            process_data = {
                "action": "add",
                "program_details": {
                    "name": "Discovered Program",
                    "description": "Discovered through automated search"
                }
            }
            response = client.post(f"/api/discovery/{discovery_id}/items/{item_id}/process", json=process_data)
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == item_id
            assert data["processed"] == True
            assert data["added_to_index"] == True
        else:
            # Skip this test if no items are available
            pytest.skip("No discovery items available to process")
