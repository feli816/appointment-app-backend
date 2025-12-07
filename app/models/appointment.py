from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Appointment(SQLModel, table=True):
    __tablename__ = "appointments"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(index=True, foreign_key="tenants.id")
    service_id: int = Field(foreign_key="services.id")
    user_id: int = Field(foreign_key="users.id")
    start_datetime: datetime
    end_datetime: datetime
    status: str
