"""Configuração de logs estruturados (JSON) — alimenta `/admin/logs`.

Schema canônico em docs/screens/logs-screen.spec.md.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

import structlog


def configure_logging(level: str = "info", service: str = "api", env: str = "development") -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=log_level)

    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="ts"),
        _add_static_fields(service=service, env=env),
        _drop_pii,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def _add_static_fields(service: str, env: str) -> Any:
    def _proc(_logger: Any, _name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        event_dict.setdefault("service", service)
        event_dict.setdefault("env", env)
        event_dict.setdefault("category", "app")
        return event_dict

    return _proc


_PII_KEYS = {"password", "senha", "cpf", "cardNumber", "card_number", "cvv", "token", "authorization"}


def _drop_pii(_logger: Any, _name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """Remove campos sensíveis comuns. Defesa em profundidade — não substitui revisão."""
    for k in list(event_dict.keys()):
        if k.lower() in _PII_KEYS:
            event_dict[k] = "***"
    return event_dict


def get_logger(name: str | None = None) -> Any:
    return structlog.get_logger(name)
