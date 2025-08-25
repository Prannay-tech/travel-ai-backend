"""
Simple test file for the Travel AI Backend
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_chat_endpoint():
    """Test the chat endpoint"""
    response = client.post("/chat", json={
        "message": "Hello",
        "conversation_history": []
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

if __name__ == "__main__":
    pytest.main([__file__])
