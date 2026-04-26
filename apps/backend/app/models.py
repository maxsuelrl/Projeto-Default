"""Modelos SQLAlchemy — schema base do template."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def _uuid() -> uuid.UUID:
    return uuid.uuid4()


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class TechLog(Base):
    """Log técnico — alimenta /admin/logs.

    Em produção, a fonte real são os JSON em stdout coletados por sink externo
    (Loki/CloudWatch). Esta tabela serve como buffer local para
    desenvolvimento e como sink padrão quando não há observability stack.
    """

    __tablename__ = "tech_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
    level: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    service: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    env: Mapped[str] = mapped_column(String(16), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    event: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    message: Mapped[str] = mapped_column(String(2000), nullable=False)
    trace_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    request_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    route: Mapped[str | None] = mapped_column(String(255), nullable=True)
    method: Mapped[str | None] = mapped_column(String(10), nullable=True)
    status: Mapped[int | None] = mapped_column(nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(nullable=True)
    outcome: Mapped[str | None] = mapped_column(String(16), nullable=True)
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    context: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)


class AuditEvent(Base):
    """Evento de auditoria — alimenta /admin/audit-logs.

    Append-only por contrato (trigger de UPDATE/DELETE bloqueia em
    Alembic). Cada linha referencia o hash da anterior (cadeia de
    integridade). Ver docs/screens/audit-logs-screen.spec.md.
    """

    __tablename__ = "audit_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
    actor: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    entity: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    before: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    after: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False, default="ok")
    reason: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    trace_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    prev_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
