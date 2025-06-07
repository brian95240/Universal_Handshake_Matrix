import pytest
from fastapi.testclient import TestClient
from ..app import app

client = TestClient(app)

class TestBudgetsAPI:
    """Test cases for the Budgets API endpoints."""
    
    def test_list_budgets(self):
        """Test retrieving a paginated list of budgets."""
        response = client.get("/api/budgets")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert isinstance(data["data"], list)
    
    def test_list_budgets_with_filters(self):
        """Test retrieving budgets with filters."""
        response = client.get("/api/budgets", params={
            "status": "active",
            "startDate": "2025-01-01T00:00:00Z",
            "endDate": "2025-12-31T23:59:59Z"
        })
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
    
    def test_create_budget(self):
        """Test creating a new budget."""
        budget_data = {
            "name": "Q2 Marketing Budget",
            "total_amount": 10000,
            "currency": "USD",
            "start_date": "2025-04-01T00:00:00Z",
            "end_date": "2025-06-30T23:59:59Z",
            "allocations": [
                {
                    "target_type": "category",
                    "target_id": "electronics",
                    "amount": 5000
                },
                {
                    "target_type": "category",
                    "target_id": "fashion",
                    "amount": 5000
                }
            ]
        }
        response = client.post("/api/budgets", json=budget_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == budget_data["name"]
        assert "id" in data
        assert data["status"] == "active"
        assert len(data["allocations"]) == 2
    
    def test_get_budget(self):
        """Test retrieving a specific budget."""
        # First create a budget
        budget_data = {
            "name": "Q2 Marketing Budget",
            "total_amount": 10000,
            "currency": "USD",
            "start_date": "2025-04-01T00:00:00Z",
            "end_date": "2025-06-30T23:59:59Z",
            "allocations": [
                {
                    "target_type": "category",
                    "target_id": "electronics",
                    "amount": 5000
                }
            ]
        }
        create_response = client.post("/api/budgets", json=budget_data)
        budget_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/budgets/{budget_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == budget_id
        assert data["name"] == budget_data["name"]
    
    def test_update_budget(self):
        """Test updating an existing budget."""
        # First create a budget
        budget_data = {
            "name": "Q2 Marketing Budget",
            "total_amount": 10000,
            "currency": "USD",
            "start_date": "2025-04-01T00:00:00Z",
            "end_date": "2025-06-30T23:59:59Z",
            "allocations": [
                {
                    "target_type": "category",
                    "target_id": "electronics",
                    "amount": 5000
                }
            ]
        }
        create_response = client.post("/api/budgets", json=budget_data)
        budget_id = create_response.json()["id"]
        
        # Then update it
        update_data = {
            "name": "Updated Q2 Budget",
            "total_amount": 15000
        }
        response = client.put(f"/api/budgets/{budget_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == budget_id
        assert data["name"] == update_data["name"]
        assert data["total_amount"] == update_data["total_amount"]
    
    def test_delete_budget(self):
        """Test deleting a budget."""
        # First create a budget
        budget_data = {
            "name": "Q2 Marketing Budget",
            "total_amount": 10000,
            "currency": "USD",
            "start_date": "2025-04-01T00:00:00Z",
            "end_date": "2025-06-30T23:59:59Z",
            "allocations": [
                {
                    "target_type": "category",
                    "target_id": "electronics",
                    "amount": 5000
                }
            ]
        }
        create_response = client.post("/api/budgets", json=budget_data)
        budget_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(f"/api/budgets/{budget_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/api/budgets/{budget_id}")
        assert get_response.status_code == 404
    
    def test_update_budget_status(self):
        """Test updating the status of a budget."""
        # First create a budget
        budget_data = {
            "name": "Q2 Marketing Budget",
            "total_amount": 10000,
            "currency": "USD",
            "start_date": "2025-04-01T00:00:00Z",
            "end_date": "2025-06-30T23:59:59Z",
            "allocations": [
                {
                    "target_type": "category",
                    "target_id": "electronics",
                    "amount": 5000
                }
            ]
        }
        create_response = client.post("/api/budgets", json=budget_data)
        budget_id = create_response.json()["id"]
        
        # Then update its status
        status_data = {
            "status": "paused"
        }
        response = client.post(f"/api/budgets/{budget_id}/status", json=status_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == budget_id
        assert data["status"] == status_data["status"]
