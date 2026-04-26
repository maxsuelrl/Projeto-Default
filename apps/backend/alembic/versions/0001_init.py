"""schema inicial: users, tech_logs, audit_events (append-only).

Revision ID: 0001
Revises:
Create Date: 2026-04-26
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID


revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(320), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(32), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "tech_logs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("ts", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("level", sa.String(16), nullable=False),
        sa.Column("service", sa.String(64), nullable=False),
        sa.Column("env", sa.String(16), nullable=False),
        sa.Column("category", sa.String(32), nullable=False),
        sa.Column("event", sa.String(128), nullable=False),
        sa.Column("message", sa.String(2000), nullable=False),
        sa.Column("trace_id", sa.String(64), nullable=True),
        sa.Column("user_id", UUID(as_uuid=True), nullable=True),
        sa.Column("request_id", sa.String(64), nullable=True),
        sa.Column("route", sa.String(255), nullable=True),
        sa.Column("method", sa.String(10), nullable=True),
        sa.Column("status", sa.Integer, nullable=True),
        sa.Column("latency_ms", sa.Integer, nullable=True),
        sa.Column("outcome", sa.String(16), nullable=True),
        sa.Column("error_code", sa.String(64), nullable=True),
        sa.Column("context", JSONB, nullable=True),
    )
    op.create_index("ix_tech_logs_ts", "tech_logs", ["ts"])
    op.create_index("ix_tech_logs_level", "tech_logs", ["level"])
    op.create_index("ix_tech_logs_service", "tech_logs", ["service"])
    op.create_index("ix_tech_logs_category", "tech_logs", ["category"])
    op.create_index("ix_tech_logs_event", "tech_logs", ["event"])
    op.create_index("ix_tech_logs_trace_id", "tech_logs", ["trace_id"])
    op.create_index("ix_tech_logs_user_id", "tech_logs", ["user_id"])

    op.create_table(
        "audit_events",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("ts", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("actor", JSONB, nullable=False),
        sa.Column("action", sa.String(128), nullable=False),
        sa.Column("entity", JSONB, nullable=False),
        sa.Column("before", JSONB, nullable=True),
        sa.Column("after", JSONB, nullable=True),
        sa.Column("outcome", sa.String(16), nullable=False, server_default="ok"),
        sa.Column("reason", sa.String(2000), nullable=True),
        sa.Column("request_id", sa.String(64), nullable=True),
        sa.Column("trace_id", sa.String(64), nullable=True),
        sa.Column("prev_hash", sa.String(64), nullable=True),
        sa.Column("hash", sa.String(64), nullable=False),
    )
    op.create_index("ix_audit_events_ts", "audit_events", ["ts"])
    op.create_index("ix_audit_events_action", "audit_events", ["action"])
    op.create_index("ix_audit_events_request_id", "audit_events", ["request_id"])
    op.create_index("ix_audit_events_trace_id", "audit_events", ["trace_id"])
    op.create_index("ix_audit_events_hash", "audit_events", ["hash"])

    # Trigger: bloqueia UPDATE/DELETE em audit_events (append-only por contrato).
    op.execute(
        """
        CREATE OR REPLACE FUNCTION audit_events_block_modify() RETURNS trigger AS $$
        BEGIN
          RAISE EXCEPTION 'audit_events is append-only (op=%, by=%)',
            TG_OP, current_user
            USING ERRCODE = 'integrity_constraint_violation';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        "CREATE TRIGGER audit_events_no_update BEFORE UPDATE ON audit_events "
        "FOR EACH ROW EXECUTE FUNCTION audit_events_block_modify();"
    )
    op.execute(
        "CREATE TRIGGER audit_events_no_delete BEFORE DELETE ON audit_events "
        "FOR EACH ROW EXECUTE FUNCTION audit_events_block_modify();"
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS audit_events_no_delete ON audit_events")
    op.execute("DROP TRIGGER IF EXISTS audit_events_no_update ON audit_events")
    op.execute("DROP FUNCTION IF EXISTS audit_events_block_modify()")
    op.drop_table("audit_events")
    op.drop_table("tech_logs")
    op.drop_table("users")
