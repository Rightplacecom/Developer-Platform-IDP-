from fastapi import APIRouter, HTTPException

from api.schemas import DeploymentRequest
from control_plane.policy_engine import PolicyEngine, PolicyViolation
from control_plane.template_engine import TemplateEngine
from control_plane.status_service import StatusService
from control_plane.deployment_service import DeploymentService

router = APIRouter()
templates = TemplateEngine()
policy = PolicyEngine()
statuses = StatusService()
deployments = DeploymentService(statuses)
_services = {}


@router.get("/api/v1/templates")
def list_templates():
    return templates.available_templates()


@router.post("/api/v1/services")
def create_service(request: DeploymentRequest):
    try:
        policy.validate(request)
    except PolicyViolation as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    templates.render("python-fastapi", request.model_dump())
    _services[request.service_name] = request.model_dump()
    return {"service_name": request.service_name, "owner": request.owner, "status": "created"}


@router.get("/api/v1/services")
def list_services():
    return list(_services.values())


@router.get("/api/v1/services/{name}")
def get_service(name: str):
    service = _services.get(name)
    if not service:
        raise HTTPException(status_code=404, detail="service not found")
    return service


@router.post("/api/v1/services/{name}/deployments")
def start_deployment(name: str, request: DeploymentRequest):
    if request.service_name != name:
        raise HTTPException(status_code=422, detail="service name must match the URL")
    try:
        policy.validate(request)
    except PolicyViolation as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return deployments.deploy(request)


@router.get("/api/v1/services/{name}/logs")
def get_logs(name: str):
    if name not in _services:
        raise HTTPException(status_code=404, detail="service not found")
    return {"service": name, "logs": [], "message": "connect a centralized logging backend for application logs"}
