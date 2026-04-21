import pytest


class TestSignup:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """
        Test successful signup for an activity with available spots.

        Arrange: TestClient with empty activity (Basketball Team) and valid email
        Act: Send POST request to /activities/Basketball Team/signup with email
        Assert: Response status is 200, message confirms signup, and participant is added
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "jacob@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"

        # Verify participant was actually added
        verify_response = client.get("/activities")
        activities = verify_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_to_activity_not_found(self, client):
        """
        Test signup fails when activity does not exist.

        Arrange: TestClient and non-existent activity name
        Act: Send POST request to /activities/NonExistent/signup
        Assert: Response status is 404 with "Activity not found" message
        """
        # Arrange
        activity_name = "NonExistent Activity"
        email = "test@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_signup_duplicate_email(self, client):
        """
        Test signup fails when student is already signed up for the activity.

        Arrange: TestClient and Chess Club which already has michael@mergington.edu
        Act: Send POST request with michael@mergington.edu trying to signup again
        Assert: Response status is 400 with "already signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student already signed up for this activity"

    def test_signup_activity_at_capacity(self, client):
        """
        Test signup fails when activity has reached max participants.

        Arrange: Fill an activity to capacity (e.g., Basketball Team with max 15)
                 by signing up 15 different students
        Act: Try to signup one more student
        Assert: Response status is 400 with "Activity is at capacity" message
        """
        # Arrange
        activity_name = "Basketball Team"
        max_participants = 15

        # Fill the activity to capacity
        for i in range(max_participants):
            email = f"student{i}@mergington.edu"
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )

        # Try to signup one more
        overage_email = "overage@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": overage_email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Activity is at capacity"

    def test_signup_multiple_students_different_activities(self, client):
        """
        Test that students can sign up for multiple different activities.

        Arrange: TestClient with two activities and one student email
        Act: Sign up the same student for two different activities
        Assert: Both signups succeed and student appears in both activities
        """
        # Arrange
        email = "alex@mergington.edu"
        activity1 = "Basketball Team"
        activity2 = "Soccer Club"

        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

        verify_response = client.get("/activities")
        activities = verify_response.json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
