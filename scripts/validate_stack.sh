#!/usr/bin/env sh
set -eu

curl -fsS http://localhost:8000/health >/dev/null
curl -fsS http://localhost:8000/metrics >/dev/null
curl -fsS http://localhost:9090/-/ready >/dev/null
curl -fsS http://localhost:9093/-/ready >/dev/null
curl -fsS http://localhost:3000/api/health >/dev/null
curl -fsS http://localhost:8080/healthz >/dev/null
printf 'Observability stack is healthy.\n'
