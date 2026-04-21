import pytest


class TestActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_success(self, client):
        """
        Test that GET /activities returns all activities with correct structure.

        Arrange: TestClient with preset activities (reset by fixture)
        Act: Send GET request to /activities
        Assert: Response status is 200 and contains expected activities with proper structure
        """
        # Arrange
        # (reset_activities fixture ensures clean state)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Verify response is a dictionary
        assert isinstance(data, dict)
        
        # Verify expected activities are present
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Soccer Club",
            "Art Club",
            "Drama Club",
            "Debate Club",
            "Science Club"
        ]
        for activity_name in expected_activities:
            assert activity_name in data
        
        # Verify structure of each activity
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_activities_have_correct_initial_participants(self, client):
        """
        Test that activities returned have correct participant counts.

        Arrange: TestClient (reset_activities fixture)
        Act: Send GET request to /activities
        Assert: Verify specific activities have expected participant counts
        """
        # Arrange
        # (reset_activities fixture ensures clean state)

        # Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        
        # Verify participant counts for specific activities
        assert len(data["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
        
        assert len(data["Programming Class"]["participants"]) == 2
        
        # Verify empty activities
        assert len(data["Basketball Team"]["participants"]) == 0
        assert len(data["Soccer Club"]["participants"]) == 0
