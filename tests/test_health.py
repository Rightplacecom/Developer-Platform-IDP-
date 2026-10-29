from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_returns_healthy():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_failure_simulation():
    assert client.post("/simulate/failure", params={"enabled": True}).status_code == 200
    assert client.get("/health").status_code == 503
    assert client.post("/simulate/failure", params={"enabled": False}).status_code == 200
    assert client.get("/health").status_code == 200


def test_controlled_error():
    response = client.get("/simulate/error")
    assert response.status_code == 500
