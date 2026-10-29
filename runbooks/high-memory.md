# High Memory

## Diagnosis
1. Identify the host or container with growing memory usage.
2. Check recent traffic and deployments.
3. Inspect leaks, unbounded queues, caches, and dependency memory.

## Mitigation
1. Stop bounded memory tests.
2. Restart only if a leak is confirmed and restart does not lose critical state.
3. Scale or correct the memory-consuming workload.

## Recovery verification
Available memory remains above 10% and the alert resolves.
