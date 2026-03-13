from typing import Optional

from sqlmodel import SQLModel

from app.models.user import UserRole


class UserRead(SQLModel):
    id: int
    tenant_id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole


class UserCreate(SQLModel):
    tenant_id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole = UserRole.student
