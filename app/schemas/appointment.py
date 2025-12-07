from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class AppointmentRead(SQLModel):
    id: int
    tenant_id: int
    service_id: int
    user_id: int
    start_datetime: datetime
    end_datetime: datetime
    status: str


class AppointmentCreate(SQLModel):
    tenant_id: int
    service_id: int
    user_id: int
    start_datetime: datetime
    end_datetime: datetime
    status: Optional[str] = "pending"
