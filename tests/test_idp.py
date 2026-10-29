from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

VALID_REQUEST = {
    "service_name": "payments-api",
    "image": "ghcr.io/example-org/payments-api:v1.2.0",
    "environment": "dev",
    "replicas": 2,
    "port": 8000,
    "owner": "payments-team",
    "resources": {
        "cpu_request": "100m",
        "cpu_limit": "500m",
        "memory_request": "128Mi",
        "memory_limit": "512Mi",
    },
}


def test_health_and_readiness():
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 200


def test_list_templates():
    response = client.get("/api/v1/templates")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "python-fastapi"


def test_create_and_deploy_service():
    created = client.post("/api/v1/services", json=VALID_REQUEST)
    assert created.status_code == 200
    deployed = client.post("/api/v1/services/payments-api/deployments", json=VALID_REQUEST)
    assert deployed.status_code == 200
    deployment_id = deployed.json()["id"]
    status = client.get(f"/api/v1/deployments/{deployment_id}")
    assert status.status_code == 200
    assert status.json()["state"] == "READY"


def test_policy_rejects_mutable_image_tag(monkeypatch):
    request = {**VALID_REQUEST, "image": "docker.io/example/app:latest"}
    response = client.post("/api/v1/services", json=request)
    assert response.status_code == 422


def test_invalid_service_name():
    request = {**VALID_REQUEST, "service_name": "Invalid_Name"}
    response = client.post("/api/v1/services", json=request)
    assert response.status_code == 422
