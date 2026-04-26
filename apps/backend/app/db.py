"""Sessão SQLAlchemy 2.x e Base declarativa."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

_engine = create_engine(
    get_settings().database_url,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False, future=True)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
