# Service Down

## Symptoms
- `up{job="python-app"} == 0`
- The `/health` endpoint is unavailable

## Diagnosis
1. Check `docker compose ps app`.
2. Inspect `docker compose logs --tail=100 app`.
3. Check `http://localhost:8000/health`.
4. Verify the app, network, and Prometheus target configuration.

## Mitigation
1. Restart the app: `docker compose restart app`.
2. If configuration or deployment is suspect, roll back the last change.
3. Confirm readiness after restart.

## Recovery verification
1. Prometheus target becomes `UP`.
2. `/health` returns HTTP 200.
3. `ServiceDown` resolves in Alertmanager.
