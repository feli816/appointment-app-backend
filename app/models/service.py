from typing import Optional
from sqlmodel import Field, SQLModel


class Service(SQLModel, table=True):
    __tablename__ = "services"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(index=True, foreign_key="tenants.id")
    name: str
    duration_minutes: int
