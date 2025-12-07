from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(index=True, foreign_key="tenants.id")

    name: Optional[str] = None
    email: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = Field(default=None, index=True)

    otp_code: Optional[str] = None
    otp_expiration: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
