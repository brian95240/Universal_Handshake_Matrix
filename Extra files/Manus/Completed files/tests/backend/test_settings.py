import pytest
from fastapi.testclient import TestClient
from ..app import app

client = TestClient(app)

class TestSettingsAPI:
    """Test cases for the Settings API endpoints."""
    
    def test_get_settings(self):
        """Test retrieving user settings."""
        response = client.get("/api/settings")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "user_id" in data
        assert "theme" in data
        assert "notifications" in data
        assert "display_preferences" in data
    
    def test_update_settings(self):
        """Test updating user settings."""
        # First get current settings
        get_response = client.get("/api/settings")
        assert get_response.status_code == 200
        
        # Then update them
        update_data = {
            "theme": "dark",
            "notifications": {
                "email": True,
                "browser": False
            },
            "display_preferences": {
                "default_view": "grid",
                "table_columns": ["name", "status", "commission", "epc", "conversion_rate"],
                "graph_layout": "circular",
                "results_per_page": 50
            }
        }
        response = client.put("/api/settings", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["theme"] == update_data["theme"]
        assert data["notifications"]["email"] == update_data["notifications"]["email"]
        assert data["notifications"]["browser"] == update_data["notifications"]["browser"]
        assert data["display_preferences"]["default_view"] == update_data["display_preferences"]["default_view"]
        assert data["display_preferences"]["results_per_page"] == update_data["display_preferences"]["results_per_page"]
    
    def test_update_partial_settings(self):
        """Test updating only specific settings fields."""
        # Update only theme
        update_data = {
            "theme": "light"
        }
        response = client.put("/api/settings", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["theme"] == update_data["theme"]
        
        # Update only notifications
        update_data = {
            "notifications": {
                "email": False,
                "browser": True
            }
        }
        response = client.put("/api/settings", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["notifications"]["email"] == update_data["notifications"]["email"]
        assert data["notifications"]["browser"] == update_data["notifications"]["browser"]
