# API Reference

- `GET /health` — control-plane liveness
- `GET /ready` — dependency readiness
- `GET /api/v1/templates` — available templates
- `POST /api/v1/services` — create a validated service
- `GET /api/v1/services` — list services
- `GET /api/v1/services/{name}` — retrieve a service
- `POST /api/v1/services/{name}/deployments` — start deployment
- `GET /api/v1/deployments/{id}` — retrieve deployment status
- `POST /api/v1/deployments/{id}/rollback` — request rollback
- `GET /api/v1/services/{name}/logs` — retrieve authorized logs
