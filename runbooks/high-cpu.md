# High CPU

## Diagnosis
1. Identify high CPU by instance or container in Grafana.
2. Check request throughput and recent deployments.
3. Inspect application logs and expensive operations.
4. Correlate CPU saturation with traffic and dependency health.

## Mitigation
1. Scale or throttle workload traffic.
2. Stop bounded test CPU workloads.
3. Roll back a suspected CPU regression when justified.

## Recovery verification
CPU utilization remains below 85% for the alert duration and the alert resolves.
