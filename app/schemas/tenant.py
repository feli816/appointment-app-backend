from typing import Optional
from sqlmodel import SQLModel


class TenantRead(SQLModel):
    id: int
    name: str


class TenantCreate(SQLModel):
    name: str


class TenantUpdate(SQLModel):
    name: Optional[str] = None
