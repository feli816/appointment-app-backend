from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    tenant_id: int


class OTPVerifyRequest(BaseModel):
    email: str
    tenant_id: int
    otp: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
