from sqlmodel import SQLModel


class ServiceRead(SQLModel):
    id: int
    tenant_id: int
    name: str
    duration_minutes: int


class ServiceCreate(SQLModel):
    tenant_id: int
    name: str
    duration_minutes: int
