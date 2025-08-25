"""
Simple test file for the Travel AI Backend
"""
import pytest
import asyncio
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

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Travel AI API"

def test_chat_endpoint():
    """Test the chat endpoint"""
    response = client.post("/chat", json={
        "message": "Hello",
        "conversation_history": []
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

def test_recommendations_endpoint():
    """Test the recommendations endpoint"""
    response = client.post("/recommendations", json={
        "budget_per_person": "1000-2000",
        "people_count": "2",
        "travel_from": "New York",
        "travel_type": "international",
        "destination_type": "beach",
        "travel_dates": "December 2024",
        "currency": "USD",
        "additional_preferences": "romantic getaway"
    })
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] == True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
