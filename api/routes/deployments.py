from fastapi import APIRouter, HTTPException
from api.routes.services import deployments, statuses

router = APIRouter()


@router.get("/api/v1/deployments/{deployment_id}")
def deployment_status(deployment_id: str):
    record = statuses.get(deployment_id)
    if not record:
        raise HTTPException(status_code=404, detail="deployment not found")
    return record


@router.post("/api/v1/deployments/{deployment_id}/rollback")
def rollback(deployment_id: str):
    record = deployments.rollback(deployment_id)
    if not record:
        raise HTTPException(status_code=404, detail="deployment not found")
    return record
