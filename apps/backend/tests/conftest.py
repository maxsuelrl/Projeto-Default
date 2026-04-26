"""Conftest: faz JSONB compilar para JSON quando o dialeto é SQLite.

Permite rodar testes que exercitam a mecânica do hash chain sem precisar
de Postgres em todo ambiente local. CI usa Postgres real (services do
GitHub Actions) — isso é só para `pytest -x` rápido localmente.
"""

from __future__ import annotations

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.sqlite.base import SQLiteTypeCompiler


def _visit_jsonb(self, _type, **_kw) -> str:
    return "JSON"


SQLiteTypeCompiler.visit_JSONB = _visit_jsonb  # type: ignore[attr-defined]
JSONB.cache_ok = True
