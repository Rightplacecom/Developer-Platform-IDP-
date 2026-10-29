import re

from api.schemas import DeploymentRequest

CPU_RE = re.compile(r"^(?:[1-9]\d{0,3}m|[1-9]\d*(?:\.\d+)?)$")
MEMORY_RE = re.compile(r"^(?:[1-9]\d*(?:Mi|Gi))$")
ALLOWED_REGISTRIES = ("ghcr.io/", "docker.io/library/")


class PolicyViolation(ValueError):
    pass


class PolicyEngine:
    def validate(self, request: DeploymentRequest) -> None:
        if request.environment == "production" and request.replicas < 2:
            raise PolicyViolation("production deployments require at least 2 replicas")
        for value in (
            request.resources.cpu_request,
            request.resources.cpu_limit,
            request.resources.memory_request,
            request.resources.memory_limit,
        ):
            if not (CPU_RE.fullmatch(value) or MEMORY_RE.fullmatch(value)):
                raise PolicyViolation(f"invalid resource quantity: {value}")
        approved_registry = request.image.startswith(ALLOWED_REGISTRIES)
        image_part = request.image.rsplit("/", 1)[-1]
        immutable_digest = "@sha256:" in request.image
        tagged = ":" in image_part and not image_part.endswith(":latest")
        if not approved_registry or not (immutable_digest or tagged):
            raise PolicyViolation("image must use an approved registry and include a tag or digest; latest is not allowed")
