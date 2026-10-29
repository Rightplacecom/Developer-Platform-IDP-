<<<<<<< HEAD
# Internal Developer Platform (IDP)

**Build. Deploy. Observe. Scale.**

A self-service application deployment control plane built with FastAPI, Kubernetes, Docker, Terraform, and GitHub Actions.

## Capabilities

- Validated service deployment requests
- Reusable Python FastAPI templates
- Standardized Kubernetes resources, probes, security contexts, and rollouts
- Policy enforcement for names, registries, resource quantities, and replicas
- Deployment status and rollback APIs
- Namespace-scoped Kubernetes RBAC examples
- CI, Docker, Terraform, documentation, and local validation scaffolding

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Control-plane liveness |
| GET | `/ready` | Dependency readiness |
| GET | `/api/v1/templates` | List templates |
| POST | `/api/v1/services` | Create a service |
| GET | `/api/v1/services` | List services |
| GET | `/api/v1/services/{name}` | Retrieve a service |
| POST | `/api/v1/services/{name}/deployments` | Start a deployment |
| GET | `/api/v1/deployments/{id}` | Retrieve deployment status |
| POST | `/api/v1/deployments/{id}/rollback` | Request a rollback |
| GET | `/api/v1/services/{name}/logs` | Retrieve authorized logs |

## Local Development

```sh
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

Open `http://localhost:8000/docs`.

## Validation

```sh
pytest -q
docker compose config
terraform -chdir=terraform/environments/dev init
terraform -chdir=terraform/environments/dev validate
```

See the documents in [docs/](docs/) for architecture, API, security, and operations guidance.

## Production Note

Authentication, persistent deployment state, real Kubernetes client integration, centralized logging, image digest enforcement, and an external secrets solution are required before production use.
=======
# Developer-Platform-IDP-
>>>>>>> 2f530822f5a8e15318a5e2627938ae86ae7dfb31
