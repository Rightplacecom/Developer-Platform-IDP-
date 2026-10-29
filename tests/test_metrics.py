from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_metrics_endpoint_exposes_prometheus_data():
    response = client.get("/metrics")
    assert response.status_code == 200
    body = response.text
    assert "http_requests_total" in body
    assert "http_request_duration_seconds" in body
    assert "http_requests_in_progress" in body


def test_alert_receiver_accepts_notification():
    response = client.post("/alerts", json={"status": "firing"})
    assert response.status_code == 200
    assert response.json()["received"] is True
