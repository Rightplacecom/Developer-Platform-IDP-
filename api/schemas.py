from typing import Literal
from pydantic import BaseModel, Field


class Resources(BaseModel):
    cpu_request: str
    cpu_limit: str
    memory_request: str
    memory_limit: str


class DeploymentRequest(BaseModel):
    service_name: str = Field(pattern=r"^[a-z]([-a-z0-9]*[a-z0-9])?$", max_length=63)
    image: str = Field(min_length=1, max_length=512)
    environment: Literal["dev", "staging", "production"] = "dev"
    replicas: int = Field(default=2, ge=1, le=10)
    port: int = Field(default=8000, ge=1, le=65535)
    resources: Resources
    owner: str = Field(pattern=r"^[A-Za-z0-9._@-]+$", min_length=1, max_length=128)


class DeploymentStatus(BaseModel):
    id: str
    service_name: str
    state: str
    image: str
    message: str | None = None
