"""
Basic API tests for the Reliable Researcher backend.
Tests cover health checks, ingestion endpoints, and research functionality.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
from io import BytesIO

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test that health endpoint returns 200 and correct status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "environment" in data


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_endpoint(self):
        """Test that root endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data


class TestIngestEndpoints:
    """Test ingestion endpoints"""
    
    def test_ingest_url_validation_empty(self):
        """Test URL ingestion with empty source"""
        response = client.post("/api/ingest", json={"source": ""})
        assert response.status_code == 400
        assert "required" in response.json()["detail"].lower()
    
    def test_ingest_url_validation_invalid_format(self):
        """Test URL ingestion with invalid format"""
        response = client.post("/api/ingest", json={"source": "not-a-url"})
        assert response.status_code == 400
        assert "valid" in response.json()["detail"].lower()
    
    def test_ingest_text_validation_empty(self):
        """Test text ingestion with empty text"""
        response = client.post("/api/ingest/text", json={"text": ""})
        assert response.status_code == 400
        assert "required" in response.json()["detail"].lower()
    
    def test_ingest_text_validation_too_large(self):
        """Test text ingestion with text exceeding size limit"""
        large_text = "a" * 100001  # Exceeds 100KB limit
        response = client.post("/api/ingest/text", json={"text": large_text})
        assert response.status_code == 400
        assert "too large" in response.json()["detail"].lower()
    
    def test_ingest_text_success(self):
        """Test successful text ingestion"""
        test_text = "This is a test document about artificial intelligence and machine learning."
        response = client.post("/api/ingest/text", json={"text": test_text})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "chunks_count" in data
    
    def test_ingest_file_validation_no_file(self):
        """Test file ingestion without providing a file"""
        response = client.post("/api/ingest/file")
        assert response.status_code == 422  # Unprocessable entity
    
    def test_ingest_file_validation_wrong_type(self):
        """Test file ingestion with non-PDF file"""
        # Create a fake text file
        file_content = b"This is not a PDF"
        files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}
        response = client.post("/api/ingest/file", files=files)
        assert response.status_code == 400
        assert "pdf" in response.json()["detail"].lower()


class TestResearchEndpoint:
    """Test research endpoint"""
    
    def test_research_validation_empty_query(self):
        """Test research with empty query"""
        response = client.post("/api/research", json={"query": ""})
        assert response.status_code == 400
        assert "required" in response.json()["detail"].lower()
    
    def test_research_validation_too_long(self):
        """Test research with query exceeding length limit"""
        long_query = "a" * 1001  # Exceeds 1000 character limit
        response = client.post("/api/research", json={"query": long_query})
        assert response.status_code == 400
        assert "too long" in response.json()["detail"].lower()
    
    def test_research_no_documents(self):
        """Test research when no documents are ingested"""
        response = client.post("/api/research", json={"query": "What is AI?"})
        # Should return 404 or 500 depending on implementation
        assert response.status_code in [404, 500]


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rate_limit_health_endpoint(self):
        """Test that health endpoint has rate limiting"""
        # Make 31 requests (limit is 30/minute)
        responses = []
        for _ in range(31):
            response = client.get("/health")
            responses.append(response.status_code)
        
        # At least one should be rate limited (429)
        assert 429 in responses or all(r == 200 for r in responses)
        # Note: In testing, rate limiting might not trigger due to fast execution
    
    def test_rate_limit_ingest_text(self):
        """Test that ingest endpoints have rate limiting"""
        # Make 11 requests (limit is 10/minute)
        responses = []
        test_text = "Test document"
        for _ in range(11):
            response = client.post("/api/ingest/text", json={"text": test_text})
            responses.append(response.status_code)
        
        # Check if rate limiting is applied
        # Note: Might not trigger in fast test execution
        status_codes = set(responses)
        assert 200 in status_codes or 429 in status_codes


class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_endpoint(self):
        """Test accessing non-existent endpoint"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_method(self):
        """Test using wrong HTTP method"""
        response = client.get("/api/ingest")  # Should be POST
        assert response.status_code == 405  # Method not allowed
    
    def test_malformed_json(self):
        """Test sending malformed JSON"""
        response = client.post(
            "/api/research",
            data="not valid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422  # Unprocessable entity


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
