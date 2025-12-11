from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timedelta
import random

from app.db import get_session
from app.models.user import User
from app.models.tenant import Tenant
from app.schemas.auth import RegisterRequest, OTPVerifyRequest, TokenResponse
from app.core.config import get_settings
import jwt

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/register")
def register(payload: RegisterRequest, session: Session = Depends(get_session)):
    tenant = session.get(Tenant, payload.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    otp_code = str(random.randint(100000, 999999))
    expiration = datetime.utcnow() + timedelta(minutes=10)

    user = session.exec(select(User).where(User.email == payload.email, User.tenant_id == payload.tenant_id)).first()

    if not user:
        user = User(
            email=payload.email,
            tenant_id=payload.tenant_id,
            name=payload.email,
            otp_code=otp_code,
            otp_expiration=expiration,
        )
        session.add(user)
    else:
        user.otp_code = otp_code
        user.otp_expiration = expiration

    session.commit()

    print(f"OTP for {payload.email}: {otp_code}")  # simulate sending OTP

    return {"message": "OTP sent"}


@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp(payload: OTPVerifyRequest, session: Session = Depends(get_session)):
    user = session.exec(
        select(User).where(User.email == payload.email, User.tenant_id == payload.tenant_id)
    ).first()

    if not user or not user.otp_code:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.otp_code != payload.otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    if user.otp_expiration < datetime.utcnow():
        raise HTTPException(status_code=401, detail="OTP expired")

    token = jwt.encode(
        {"user_id": user.id, "tenant_id": user.tenant_id},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    user.otp_code = None
    user.otp_expiration = None
    session.commit()

    return TokenResponse(access_token=token, token_type="bearer")
