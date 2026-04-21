import pytest


class TestRoot:
    """Tests for the GET / endpoint."""

    def test_root_redirect(self, client):
        """
        Test that GET / redirects to /static/index.html.

        Arrange: TestClient is ready (provided by fixture)
        Act: Send GET request to /
        Assert: Response status is 307 (Temporary Redirect) and location header points to /static/index.html
        """
        # Arrange
        # (client fixture handles setup)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
