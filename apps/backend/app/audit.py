"""Audit-log: gravação append-only com cadeia de hash de integridade.

Schema canônico em `docs/screens/audit-logs-screen.spec.md`. PII é
mascarada **na gravação** (não na leitura).
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models import AuditEvent

_PII_FIELDS = {"password", "senha", "token", "cardNumber", "card_number", "cvv"}
_CPF_LIKE = {"cpf"}


def _mask_value(key: str, value: Any) -> Any:
    if value is None:
        return value
    k = key.lower()
    if k in _PII_FIELDS:
        return "***"
    if k in _CPF_LIKE and isinstance(value, str) and len(value) >= 4:
        return f"***.***.***-{value[-2:]}"
    if k == "email" and isinstance(value, str) and "@" in value:
        local, _, dom = value.partition("@")
        masked_local = (local[0] + "***") if local else "***"
        return f"{masked_local}@{dom}"
    return value


def _mask(d: dict[str, Any] | None) -> dict[str, Any] | None:
    if d is None:
        return None
    out: dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out[k] = _mask(v)
        else:
            out[k] = _mask_value(k, v)
    return out


def _compute_hash(prev_hash: str | None, payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    h = hashlib.sha256()
    h.update((prev_hash or "").encode("utf-8"))
    h.update(canonical.encode("utf-8"))
    return h.hexdigest()


def emit_audit(
    db: Session,
    *,
    actor: dict[str, Any],
    action: str,
    entity: dict[str, Any],
    before: dict[str, Any] | None = None,
    after: dict[str, Any] | None = None,
    outcome: str = "ok",
    reason: str | None = None,
    request_id: str | None = None,
    trace_id: str | None = None,
) -> AuditEvent:
    """Grava um evento auditável.

    A gravação é append-only — UPDATE/DELETE são bloqueados por trigger no
    Postgres (ver migrations/0001_init.py).
    """
    masked_actor = _mask(actor) or {}
    masked_entity = _mask(entity) or {}
    masked_before = _mask(before)
    masked_after = _mask(after)

    last_stmt = select(AuditEvent).order_by(desc(AuditEvent.ts)).limit(1)
    last = db.execute(last_stmt).scalar_one_or_none()
    prev_hash = last.hash if last else None

    payload = {
        "actor": masked_actor,
        "action": action,
        "entity": masked_entity,
        "before": masked_before,
        "after": masked_after,
        "outcome": outcome,
        "reason": reason,
        "request_id": request_id,
        "trace_id": trace_id,
    }
    h = _compute_hash(prev_hash, payload)

    event = AuditEvent(
        actor=masked_actor,
        action=action,
        entity=masked_entity,
        before=masked_before,
        after=masked_after,
        outcome=outcome,
        reason=reason,
        request_id=request_id,
        trace_id=trace_id,
        prev_hash=prev_hash,
        hash=h,
    )
    db.add(event)
    db.flush()
    return event


def verify_chain(db: Session, limit: int = 1000) -> tuple[bool, int]:
    """Verifica integridade dos últimos N eventos. Retorna (ok, posição_falha)."""
    rows = db.execute(
        select(AuditEvent).order_by(AuditEvent.ts.asc()).limit(limit)
    ).scalars().all()
    prev_hash: str | None = None
    for idx, row in enumerate(rows):
        payload = {
            "actor": row.actor,
            "action": row.action,
            "entity": row.entity,
            "before": row.before,
            "after": row.after,
            "outcome": row.outcome,
            "reason": row.reason,
            "request_id": row.request_id,
            "trace_id": row.trace_id,
        }
        expected = _compute_hash(prev_hash, payload)
        if expected != row.hash or row.prev_hash != prev_hash:
            return (False, idx)
        prev_hash = row.hash
    return (True, len(rows))
