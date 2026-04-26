"""Entry point do FastAPI.

Aplica:
- CORS restrito (lista do settings)
- Headers de segurança e CSP
- Rate limiting via SlowAPI
- Logs estruturados (request id correlacionável com /admin/logs)
"""

from __future__ import annotations

import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.config import get_settings
from app.logging_config import configure_logging, get_logger
from app.routers import audit_logs, auth, health, logs, manual

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    configure_logging(level=settings.log_level, service=settings.app_name, env=settings.app_env)
    get_logger().info("app.startup", env=settings.app_env)
    yield
    get_logger().info("app.shutdown")


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Projeto-Padrão API",
    version="0.1.0",
    lifespan=lifespan,
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def _ratelimit_handler(_request: Request, exc: RateLimitExceeded) -> Response:
    return Response(
        content='{"detail":"rate limit exceeded"}',
        status_code=429,
        media_type="application/json",
        headers={"Retry-After": str(getattr(exc, "retry_after", 60))},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-Id"],
)


@app.middleware("http")
async def _logging_and_security_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(requestId=request_id, route=request.url.path)

    start = time.perf_counter()
    log = get_logger("http")
    try:
        response: Response = await call_next(request)
    except Exception:
        log.exception(
            "http.request",
            method=request.method,
            status=500,
            outcome="error",
        )
        raise

    latency_ms = int((time.perf_counter() - start) * 1000)

    response.headers["X-Request-Id"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'"
    )

    log.info(
        "http.request",
        method=request.method,
        status=response.status_code,
        latencyMs=latency_ms,
        outcome="ok" if response.status_code < 500 else "error",
        category="app",
    )
    return response


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(manual.router)
app.include_router(logs.router)
app.include_router(audit_logs.router)
