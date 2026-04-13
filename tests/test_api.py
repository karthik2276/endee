import pytest

def test_root_endpoint(client):
    """Test the root API endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["service"] == "AI Complaint Assistant"

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "total_complaints" in data
    # Value is mocked to 42 in conftest.py
    assert data["total_complaints"] == 42

def test_add_complaint_validation(client):
    """Test validation for adding a complaint."""
    # Invalid request (too short)
    response = client.post("/add-complaint", json={"text": "abc", "category": "billing"})
    assert response.status_code == 422
    
    # Valid request
    response = client.post("/add-complaint", json={"text": "This is a valid complaint about the service.", "category": "support"})
    assert response.status_code == 200
    assert response.json()["message"] == "Complaint recorded and indexed."

@pytest.mark.asyncio
async def test_search_endpoint(client):
    """Test the semantic search endpoint."""
    response = client.post("/search", json={"query": "lost package", "top_k": 3})
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "results" in data

@pytest.mark.asyncio
async def test_ask_endpoint(client):
    """Test the AI chat (RAG) endpoint."""
    response = client.post("/ask", json={"question": "How do I return a broken item?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "This is a mock AI response."
