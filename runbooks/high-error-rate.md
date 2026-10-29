# High Error Rate

## Diagnosis
1. Inspect routes and status labels in Prometheus/Grafana.
2. Correlate 5xx activity with deployments and dependency failures.
3. Inspect application logs and downstream service health.

## Mitigation
1. Roll back a suspected regression if safe.
2. Restore dependencies or disable a failing optional dependency.
3. Stop controlled error-generation traffic.

## Recovery verification
5xx rate remains below 5% with sufficient traffic and the alert resolves.
