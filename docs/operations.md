# Operations

Start locally with:

`docker compose up -d --build`

Check health with `curl http://localhost:8000/health` and readiness with `curl http://localhost:8000/ready`.

For stuck deployments, inspect status, pod conditions, scheduling, image pulls, probes, and events. Roll back after confirming a release regression.
