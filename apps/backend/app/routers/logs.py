"""Endpoint para a tela `/admin/logs` (técnicos).

Em produção, conecte ao sink real (Loki/CloudWatch/Datadog). Aqui retornamos
da tabela `tech_logs` quando ela existe — útil em dev e para o spec rodar.
"""

from __future__ import annotations

import base64
import json
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_roles
from app.models import TechLog, User

router = APIRouter(prefix="/admin/logs", tags=["admin"])


@router.get("")
def list_logs(
    db: Annotated[Session, Depends(get_db)],
    _user: User = Depends(require_roles("admin", "operator")),
    level: str | None = Query(None),
    service: str | None = Query(None),
    category: str | None = Query(None),
    user_id: str | None = Query(None),
    trace_id: str | None = Query(None),
    q: str | None = Query(None),
    cursor: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
) -> dict[str, Any]:
    stmt = select(TechLog).order_by(desc(TechLog.ts), desc(TechLog.id))
    if level:
        stmt = stmt.where(TechLog.level == level)
    if service:
        stmt = stmt.where(TechLog.service == service)
    if category:
        stmt = stmt.where(TechLog.category == category)
    if user_id:
        stmt = stmt.where(TechLog.user_id == user_id)
    if trace_id:
        stmt = stmt.where(TechLog.trace_id == trace_id)
    if q:
        stmt = stmt.where(TechLog.message.ilike(f"%{q}%"))

    if cursor:
        try:
            decoded = json.loads(base64.urlsafe_b64decode(cursor).decode())
            stmt = stmt.where(TechLog.ts < datetime.fromisoformat(decoded["ts"]))
        except Exception:  # noqa: BLE001
            pass

    rows = db.execute(stmt.limit(limit + 1)).scalars().all()
    has_more = len(rows) > limit
    rows = rows[:limit]

    next_cursor: str | None = None
    if has_more and rows:
        token = json.dumps({"ts": rows[-1].ts.isoformat()}).encode()
        next_cursor = base64.urlsafe_b64encode(token).decode()

    return {
        "items": [
            {
                "id": str(r.id),
                "ts": r.ts.isoformat(),
                "level": r.level,
                "service": r.service,
                "env": r.env,
                "category": r.category,
                "event": r.event,
                "message": r.message,
                "traceId": r.trace_id,
                "userId": str(r.user_id) if r.user_id else None,
                "requestId": r.request_id,
                "route": r.route,
                "method": r.method,
                "status": r.status,
                "latencyMs": r.latency_ms,
                "outcome": r.outcome,
                "errorCode": r.error_code,
                "context": r.context,
            }
            for r in rows
        ],
        "nextCursor": next_cursor,
    }
