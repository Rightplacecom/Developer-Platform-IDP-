from fastapi import FastAPI

from api.routes.deployments import router as deployment_router
from api.routes.services import router as service_router

app = FastAPI(
    title="Internal Developer Platform",
    version="1.0.0",
    description="Self-service Kubernetes deployment control plane",
)

app.include_router(service_router)
app.include_router(deployment_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "idp-control-plane"}


@app.get("/ready")
def readiness():
    return {"status": "ready"}
