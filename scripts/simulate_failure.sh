#!/usr/bin/env sh
set -eu

case "${1:-error}" in
  app-down)
    docker compose stop app
    ;;
  app-up)
    docker compose start app
    ;;
  error)
    curl -fsS -X POST 'http://localhost:8000/simulate/failure?enabled=true' >/dev/null
    ;;
  recover)
    curl -fsS -X POST 'http://localhost:8000/simulate/failure?enabled=false' >/dev/null
    ;;
  *)
    echo "Usage: $0 {app-down|app-up|error|recover}"
    exit 1
    ;;
esac
