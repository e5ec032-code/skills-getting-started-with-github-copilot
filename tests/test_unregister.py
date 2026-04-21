import pytest


class TestUnregister:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client):
        """
        Test successful unregistration from an activity.

        Arrange: TestClient with Chess Club which has michael@mergington.edu
        Act: Send DELETE request to unregister michael@mergington.edu
        Assert: Response status is 200, message confirms unregister, and participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Unregistered {email} from {activity_name}"

        # Verify participant was actually removed
        verify_response = client.get("/activities")
        activities = verify_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_activity_not_found(self, client):
        """
        Test unregister fails when activity does not exist.

        Arrange: TestClient and non-existent activity name
        Act: Send DELETE request to /activities/NonExistent/unregister
        Assert: Response status is 404 with "Activity not found" message
        """
        # Arrange
        activity_name = "NonExistent Activity"
        email = "test@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_unregister_student_not_signed_up(self, client):
        """
        Test unregister fails when student is not signed up for the activity.

        Arrange: TestClient and an activity (Basketball Team) where student is not signed up
        Act: Send DELETE request with email not in participants list
        Assert: Response status is 400 with "not signed up" message
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student not signed up for this activity"

    def test_unregister_then_resign_up(self, client):
        """
        Test that a student can unregister and then sign up again for the same activity.

        Arrange: TestClient with Chess Club participant
        Act: Unregister the participant, then sign them up again
        Assert: Both operations succeed and final participant list includes the student
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Act - Sign up again
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200

        # Verify student is in participants after re-signup
        verify_response = client.get("/activities")
        activities = verify_response.json()
        assert email in activities[activity_name]["participants"]

    def test_unregister_frees_capacity_slot(self, client):
        """
        Test that unregistering a student frees up a capacity slot for others.

        Arrange: Fill an activity to capacity, then unregister one student
        Act: Try to sign up a new student after unregister
        Assert: The new signup succeeds (slot is now available)
        """
        # Arrange
        activity_name = "Basketball Team"
        max_participants = 15

        # Fill the activity to capacity
        students = []
        for i in range(max_participants):
            email = f"student{i}@mergington.edu"
            students.append(email)
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )

        # Unregister the first student to free up a slot
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": students[0]}
        )

        # Try to sign up a new student
        new_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert
        assert response.status_code == 200
        verify_response = client.get("/activities")
        activities = verify_response.json()
        assert new_email in activities[activity_name]["participants"]
        assert students[0] not in activities[activity_name]["participants"]
