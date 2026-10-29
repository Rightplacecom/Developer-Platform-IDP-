# Architecture

The FastAPI control plane validates developer requests, renders approved templates, and coordinates Kubernetes deployment lifecycle operations. Kubernetes schedules and owns workload recovery.

Deployment state transitions are REQUESTED, VALIDATING, DEPLOYING, READY, FAILED, ROLLING_BACK, and ROLLED_BACK. Production authentication and persistent status storage must be added before production use.
