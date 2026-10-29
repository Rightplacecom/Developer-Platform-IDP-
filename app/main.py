import os
import time
import threading
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Production Observability Demo")

REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "route", "status"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "route"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)
IN_PROGRESS = Gauge("http_requests_in_progress", "HTTP requests currently in progress")
ALERT_NOTIFICATIONS = Counter("alert_notifications_received_total", "Alert notifications received from Alertmanager", ["status"])
FAILED_STATE = False

@app.middleware("http")
async def observe_requests(request: Request, call_next):
    global FAILED_STATE
    IN_PROGRESS.inc()
    started = time.perf_counter()
    try:
        response = await call_next(request)
        status = str(response.status_code)
    except Exception:
        status = "500"
        raise
    finally:
        elapsed = time.perf_counter() - started
        route = request.scope.get("route")
        route_name = getattr(route, "path", request.url.path)
        REQUESTS.labels(request.method, route_name, status).inc()
        REQUEST_DURATION.labels(request.method, route_name).observe(elapsed)
        IN_PROGRESS.dec()
    return response

@app.get("/health")
async def health():
    if FAILED_STATE:
        return JSONResponse(status_code=503, content={"status": "unhealthy"})
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    return {"status": "ready"}

@app.get("/")
async def root():
    return {"service": "production-observability-platform", "status": "running"}

@app.post("/simulate/failure")
async def simulate_failure(enabled: bool = True):
    global FAILED_STATE
    FAILED_STATE = enabled
    return {"failure_simulation": "enabled" if enabled else "disabled"}

@app.get("/simulate/error")
async def simulate_error():
    return JSONResponse(status_code=500, content={"error": "controlled test failure"})

@app.get("/simulate/latency")
async def simulate_latency(milliseconds: int = 600):
    milliseconds = min(max(milliseconds, 0), 5000)
    time.sleep(milliseconds / 1000)
    return {"latency_ms": milliseconds}

@app.get("/simulate/cpu")
async def simulate_cpu(seconds: int = 5):
    seconds = min(max(seconds, 1), 30)
    end = time.perf_counter() + seconds
    while time.perf_counter() < end:
        _ = sum(i * i for i in range(10000))
    return {"cpu_burn_seconds": seconds}

@app.post("/alerts")
async def receive_alert(payload: dict):
    status = payload.get("status", "unknown")
    ALERT_NOTIFICATIONS.labels(status=status).inc()
    return {"received": True, "status": status}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
