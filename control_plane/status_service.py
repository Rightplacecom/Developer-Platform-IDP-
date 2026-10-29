from threading import Lock
from uuid import uuid4


class StatusService:
    def __init__(self):
        self._deployments = {}
        self._lock = Lock()

    def create(self, service_name: str, image: str) -> dict:
        deployment_id = str(uuid4())
        record = {"id": deployment_id, "service_name": service_name, "state": "REQUESTED", "image": image, "message": None}
        with self._lock:
            self._deployments[deployment_id] = record
        return record.copy()

    def get(self, deployment_id: str) -> dict | None:
        with self._lock:
            record = self._deployments.get(deployment_id)
            return record.copy() if record else None

    def transition(self, deployment_id: str, state: str, message: str | None = None) -> dict | None:
        with self._lock:
            record = self._deployments.get(deployment_id)
            if not record:
                return None
            record["state"] = state
            record["message"] = message
            return record.copy()
