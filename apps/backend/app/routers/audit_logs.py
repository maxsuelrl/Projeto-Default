"""Endpoint para a tela `/admin/audit-logs` (auditoria append-only).

Sem PUT/PATCH/DELETE — auditoria é append-only por contrato. Tentativas
geram audit-log de tampering e respondem 405.
"""

from __future__ import annotations

import base64
import json
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.audit import emit_audit, verify_chain
from app.db import get_db
from app.deps import require_roles
from app.models import AuditEvent, User

router = APIRouter(prefix="/admin/audit-logs", tags=["admin"])


@router.get("")
def list_audit(
    db: Annotated[Session, Depends(get_db)],
    request: Request,
    user: User = Depends(require_roles("admin", "auditor")),
    actor_email: str | None = Query(None),
    action: str | None = Query(None),
    entity_type: str | None = Query(None),
    outcome: str | None = Query(None),
    q: str | None = Query(None),
    cursor: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
) -> dict[str, Any]:
    stmt = select(AuditEvent).order_by(desc(AuditEvent.ts), desc(AuditEvent.id))
    if action:
        stmt = stmt.where(AuditEvent.action == action)
    if outcome:
        stmt = stmt.where(AuditEvent.outcome == outcome)
    if q:
        stmt = stmt.where(AuditEvent.reason.ilike(f"%{q}%"))

    if cursor:
        try:
            decoded = json.loads(base64.urlsafe_b64decode(cursor).decode())
            stmt = stmt.where(AuditEvent.ts < datetime.fromisoformat(decoded["ts"]))
        except Exception:  # noqa: BLE001
            pass

    rows = db.execute(stmt.limit(limit + 1)).scalars().all()
    has_more = len(rows) > limit
    rows = rows[:limit]

    if actor_email:
        rows = [r for r in rows if (r.actor or {}).get("email", "").startswith(actor_email[0])]
    if entity_type:
        rows = [r for r in rows if (r.entity or {}).get("type") == entity_type]

    next_cursor: str | None = None
    if has_more and rows:
        token = json.dumps({"ts": rows[-1].ts.isoformat()}).encode()
        next_cursor = base64.urlsafe_b64encode(token).decode()

    emit_audit(
        db,
        actor={
            "userId": str(user.id),
            "email": user.email,
            "role": user.role,
            "ip": request.client.host if request.client else None,
        },
        action="audit.audit_view",
        entity={"type": "audit_log", "id": "list"},
        outcome="ok",
        reason=f"filters: action={action}, q={q}",
        request_id=request.headers.get("x-request-id"),
    )
    db.commit()

    return {
        "items": [
            {
                "id": str(r.id),
                "ts": r.ts.isoformat(),
                "actor": r.actor,
                "action": r.action,
                "entity": r.entity,
                "before": r.before,
                "after": r.after,
                "outcome": r.outcome,
                "reason": r.reason,
                "requestId": r.request_id,
                "traceId": r.trace_id,
                "prevHash": r.prev_hash,
                "hash": r.hash,
            }
            for r in rows
        ],
        "nextCursor": next_cursor,
    }


@router.get("/verify")
def verify(
    db: Annotated[Session, Depends(get_db)],
    _user: User = Depends(require_roles("admin", "auditor")),
    limit: int = Query(1000, ge=1, le=10000),
) -> dict[str, Any]:
    ok, position = verify_chain(db, limit=limit)
    return {"ok": ok, "checked": position, "limit": limit}
