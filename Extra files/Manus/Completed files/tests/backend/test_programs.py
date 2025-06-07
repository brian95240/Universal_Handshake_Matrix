import pytest
from fastapi.testclient import TestClient
from ..app import app

client = TestClient(app)

class TestProgramsAPI:
    """Test cases for the Programs API endpoints."""
    
    def test_list_programs(self):
        """Test retrieving a paginated list of programs."""
        response = client.get("/api/programs")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert isinstance(data["data"], list)
    
    def test_list_programs_with_filters(self):
        """Test retrieving programs with filters."""
        response = client.get("/api/programs", params={
            "status": "active",
            "category": "electronics",
            "minEpc": 1.0
        })
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
    
    def test_create_program(self):
        """Test creating a new program."""
        program_data = {
            "name": "Test Program",
            "description": "Test description",
            "url": "https://example.com",
            "category": ["test"],
            "commission": {
                "type": "percentage",
                "value": 10
            },
            "cookie_duration": 30,
            "payment_frequency": "monthly",
            "minimum_payout": 50,
            "payment_methods": ["paypal"],
            "status": "active",
            "tags": ["test"],
            "source": "manual"
        }
        response = client.post("/api/programs", json=program_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == program_data["name"]
        assert "id" in data
    
    def test_get_program(self):
        """Test retrieving a specific program."""
        # First create a program
        program_data = {
            "name": "Test Program",
            "description": "Test description",
            "url": "https://example.com",
            "category": ["test"],
            "commission": {
                "type": "percentage",
                "value": 10
            },
            "cookie_duration": 30,
            "payment_frequency": "monthly",
            "minimum_payout": 50,
            "payment_methods": ["paypal"],
            "status": "active",
            "tags": ["test"],
            "source": "manual"
        }
        create_response = client.post("/api/programs", json=program_data)
        program_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/programs/{program_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == program_id
        assert data["name"] == program_data["name"]
    
    def test_update_program(self):
        """Test updating an existing program."""
        # First create a program
        program_data = {
            "name": "Test Program",
            "description": "Test description",
            "url": "https://example.com",
            "category": ["test"],
            "commission": {
                "type": "percentage",
                "value": 10
            },
            "cookie_duration": 30,
            "payment_frequency": "monthly",
            "minimum_payout": 50,
            "payment_methods": ["paypal"],
            "status": "active",
            "tags": ["test"],
            "source": "manual"
        }
        create_response = client.post("/api/programs", json=program_data)
        program_id = create_response.json()["id"]
        
        # Then update it
        update_data = {
            "name": "Updated Program",
            "description": "Updated description"
        }
        response = client.put(f"/api/programs/{program_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == program_id
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
    
    def test_delete_program(self):
        """Test deleting a program."""
        # First create a program
        program_data = {
            "name": "Test Program",
            "description": "Test description",
            "url": "https://example.com",
            "category": ["test"],
            "commission": {
                "type": "percentage",
                "value": 10
            },
            "cookie_duration": 30,
            "payment_frequency": "monthly",
            "minimum_payout": 50,
            "payment_methods": ["paypal"],
            "status": "active",
            "tags": ["test"],
            "source": "manual"
        }
        create_response = client.post("/api/programs", json=program_data)
        program_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(f"/api/programs/{program_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/api/programs/{program_id}")
        assert get_response.status_code == 404
    
    def test_get_program_metrics(self):
        """Test retrieving metrics for a specific program."""
        # First create a program
        program_data = {
            "name": "Test Program",
            "description": "Test description",
            "url": "https://example.com",
            "category": ["test"],
            "commission": {
                "type": "percentage",
                "value": 10
            },
            "cookie_duration": 30,
            "payment_frequency": "monthly",
            "minimum_payout": 50,
            "payment_methods": ["paypal"],
            "status": "active",
            "tags": ["test"],
            "source": "manual"
        }
        create_response = client.post("/api/programs", json=program_data)
        program_id = create_response.json()["id"]
        
        # Then get its metrics
        response = client.get(f"/api/programs/{program_id}/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "clicks" in data
        assert "conversions" in data
        assert "revenue" in data
        assert "roi" in data
