"""Testa cadeia de hash do audit-log com SQLite em memória."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.audit import emit_audit, verify_chain
from app.db import Base


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:", future=True)
    # JSONB não existe em SQLite — mapeia para JSON com workaround.
    from sqlalchemy.dialects import postgresql
    from sqlalchemy import JSON

    postgresql.JSONB.__visit_name__ = "JSON"  # type: ignore[attr-defined]
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    yield Session()


def test_audit_chain_grows_and_verifies(db):  # noqa: ANN001
    actor = {"userId": "u1", "email": "a@b.com", "role": "admin"}
    e1 = emit_audit(db, actor=actor, action="user.update", entity={"type": "user", "id": "u2"},
                    after={"role": "editor"})
    e2 = emit_audit(db, actor=actor, action="user.delete", entity={"type": "user", "id": "u3"})
    db.commit()

    assert e1.prev_hash is None
    assert e2.prev_hash == e1.hash
    ok, checked = verify_chain(db, limit=10)
    assert ok is True
    assert checked == 2


def test_audit_pii_masked(db):  # noqa: ANN001
    actor = {"userId": "u1", "email": "operador@empresa.com", "role": "admin"}
    e = emit_audit(
        db,
        actor=actor,
        action="auth.login",
        entity={"type": "user", "id": "u2"},
        before={"password": "p4ss", "cpf": "12345678901"},
    )
    db.commit()
    assert e.before["password"] == "***"
    assert e.before["cpf"].startswith("***.***.***-")
    assert e.actor["email"].startswith("o***@")
