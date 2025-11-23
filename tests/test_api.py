from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    """Test if the health endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_ingest_endpoint_structure():
    """Test that ingest endpoint exists and accepts files."""
    # Mocking a PDF file upload
    files = {'file': ('test.pdf', b'dummy content', 'application/pdf')}
    response = client.post("/ingest", files=files)
    assert response.status_code == 200
    assert "filename" in response.json()