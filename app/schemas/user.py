from typing import Optional
from sqlmodel import SQLModel


class UserRead(SQLModel):
    id: int
    tenant_id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(SQLModel):
    tenant_id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
