from typing import Optional

from pydantic import BaseModel

from app.models.user import UserRole


class RegisterRequest(BaseModel):
    email: str
    tenant_id: int
    name: Optional[str] = None
    role: UserRole = UserRole.student


class OTPVerifyRequest(BaseModel):
    email: str
    tenant_id: int
    otp: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
