"""Autenticação básica — login com e-mail/senha + emit de audit-log."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import emit_audit
from app.db import get_db
from app.logging_config import get_logger
from app.models import User
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])
log = get_logger("auth")


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterIn(LoginIn):
    role: str = "user"


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterIn,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> TokenOut:
    existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="email already registered")
    user = User(
        email=str(payload.email),
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.flush()

    emit_audit(
        db,
        actor={
            "userId": str(user.id),
            "email": user.email,
            "role": user.role,
            "ip": request.client.host if request.client else None,
            "userAgent": request.headers.get("user-agent"),
        },
        action="auth.register",
        entity={"type": "user", "id": str(user.id)},
        after={"email": user.email, "role": user.role, "active": True},
        outcome="ok",
        request_id=request.headers.get("x-request-id"),
    )
    db.commit()
    log.info("user.registered", user_id=str(user.id), email=user.email, category="security")
    return TokenOut(access_token=create_access_token(user.id, user.role))


@router.post("/login", response_model=TokenOut)
def login(
    payload: LoginIn,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> TokenOut:
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    actor_base = {
        "email": str(payload.email),
        "ip": request.client.host if request.client else None,
        "userAgent": request.headers.get("user-agent"),
    }

    if not user or not user.is_active or not verify_password(payload.password, user.password_hash):
        emit_audit(
            db,
            actor={**actor_base, "userId": str(user.id) if user else None},
            action="auth.login",
            entity={"type": "user", "id": str(user.id) if user else None},
            outcome="error",
            reason="invalid credentials",
            request_id=request.headers.get("x-request-id"),
        )
        db.commit()
        log.warning("auth.login.failed", email=str(payload.email), category="security")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    emit_audit(
        db,
        actor={**actor_base, "userId": str(user.id), "role": user.role},
        action="auth.login",
        entity={"type": "user", "id": str(user.id)},
        outcome="ok",
        request_id=request.headers.get("x-request-id"),
    )
    db.commit()
    log.info(
        "auth.login.ok",
        user_id=str(user.id),
        category="security",
        outcome="ok",
    )
    return TokenOut(access_token=create_access_token(user.id, user.role))
