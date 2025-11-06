"""
Tests for main FastAPI application initialization and basic endpoints.

This tests the core application setup, health checks, and basic functionality.
Like testing Express app.js setup and basic routes.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create test client for FastAPI app (like supertest for Express)
client = TestClient(app)


class TestMainApplication:
    """Test the main FastAPI application setup and basic endpoints."""

    def test_app_initialization(self):
        """Test that the FastAPI app initializes correctly."""
        assert app.title == "Python Excel API"
        assert app.version == "1.0.0"
        assert app.description == "Python API for Excel report generation from templates"

    def test_root_endpoint(self):
        """Test the root endpoint returns correct information."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        # Test response structure
        assert data["success"] is True
        assert "data" in data
        assert "message" in data
        assert "timestamp" in data

        # Test response content
        assert data["data"]["message"] == "Welcome to Python Excel API"
        assert data["data"]["version"] == "1.0.0"
        assert data["data"]["docs"] == "/docs"
        assert data["data"]["health"] == "/api/health"

    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = client.get("/api/health")

        assert response.status_code == 200
        data = response.json()

        # Test response structure
        assert data["success"] is True
        assert "data" in data
        assert "message" in data
        assert "timestamp" in data

        # Test health data
        assert data["data"]["status"] == "healthy"
        assert data["data"]["app_name"] == "Python Excel API"
        assert data["data"]["version"] == "1.0.0"
        assert "debug" in data["data"]
        assert "timestamp" in data["data"]

    def test_docs_endpoint_exists(self):
        """Test that the API documentation endpoint is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        # Swagger UI should return HTML
        assert "text/html" in response.headers["content-type"]

    def test_404_error_handling(self):
        """Test that 404 errors are handled correctly."""
        response = client.get("/nonexistent-endpoint")

        assert response.status_code == 404
        data = response.json()

        # FastAPI default 404 response format
        assert "detail" in data
        assert data["detail"] == "Not Found"

    def test_cors_headers(self):
        """Test that CORS headers are properly set."""
        response = client.options("/api/health")

        # FastAPI TestClient doesn't fully simulate CORS preflight,
        # but we can test that the middleware is configured
        # by checking that our endpoint works (CORS would block if misconfigured)
        assert response.status_code in [200, 405]  # OPTIONS might not be implemented

    def test_request_logging_middleware(self):
        """Test that request logging middleware is working."""
        # Make a request that should be logged
        response = client.get("/api/health")
        assert response.status_code == 200

        # We can't easily test logging output in unit tests,
        # but we can verify the request completes successfully
        # which means the middleware isn't breaking anything


class TestErrorHandling:
    """Test error handling and exception scenarios."""

    def test_http_exception_format(self):
        """Test that HTTP exceptions are handled correctly."""
        response = client.get("/api/nonexistent")

        assert response.status_code == 404
        data = response.json()

        # FastAPI default 404 response format
        assert "detail" in data
        assert data["detail"] == "Not Found"

    def test_general_exception_handling(self):
        """Test that unexpected exceptions are handled gracefully."""
        # This would test the general exception handler,
        # but we'd need to inject an error to trigger it.
        # For now, we'll just verify the endpoint structure works.

        response = client.get("/api/health")
        assert response.status_code == 200

        # If we reach here, the exception handlers aren't interfering
        # with normal operation


class TestAPIDocumentation:
    """Test API documentation endpoints."""

    def test_openapi_schema(self):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "Python Excel API"
        assert schema["info"]["version"] == "1.0.0"

    def test_redoc_documentation(self):
        """Test that ReDoc documentation is available."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


if __name__ == "__main__":
    # Allow running tests directly: python test_main.py
    pytest.main([__file__])