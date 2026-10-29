import hashlib
import json

from api.schemas import DeploymentRequest
from control_plane.status_service import StatusService


class DeploymentService:
    def __init__(self, status_service: StatusService):
        self.status_service = status_service
        self._deployments = {}

    def deploy(self, request: DeploymentRequest) -> dict:
        record = self.status_service.create(request.service_name, request.image)
        self.status_service.transition(record["id"], "DEPLOYING")
        payload = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": request.service_name, "labels": {"app.kubernetes.io/name": request.service_name, "app.kubernetes.io/managed-by": "idp"}},
            "spec": {
                "replicas": request.replicas,
                "selector": {"matchLabels": {"app.kubernetes.io/name": request.service_name}},
                "template": {"metadata": {"labels": {"app.kubernetes.io/name": request.service_name}}, "spec": {
                    "automountServiceAccountToken": False,
                    "securityContext": {"runAsNonRoot": True, "seccompProfile": {"type": "RuntimeDefault"}},
                    "containers": [{"name": "app", "image": request.image, "ports": [{"containerPort": request.port}], "resources": {"requests": {"cpu": request.resources.cpu_request, "memory": request.resources.memory_request}, "limits": {"cpu": request.resources.cpu_limit, "memory": request.resources.memory_limit}}}],
                }},
            },
        }
        key = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]
        self._deployments[request.service_name] = {"request": request, "manifest": payload, "revision": key}
        self.status_service.transition(record["id"], "READY")
        return self.status_service.get(record["id"])

    def rollback(self, deployment_id: str) -> dict | None:
        if not self.status_service.get(deployment_id):
            return None
        self.status_service.transition(deployment_id, "ROLLING_BACK")
        return self.status_service.transition(deployment_id, "ROLLED_BACK")
