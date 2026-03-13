from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Appointment(SQLModel, table=True):
    __tablename__ = "appointments"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(index=True, foreign_key="tenants.id")
    service_id: Optional[int] = Field(default=None, foreign_key="services.id")
    user_id: int = Field(foreign_key="users.id")  # student
    instructor_id: int = Field(foreign_key="users.id", index=True)
    slot_id: Optional[int] = Field(default=None, foreign_key="lesson_slots.id")
    start_datetime: datetime
    end_datetime: datetime
    status: str = Field(default="pending")
    meeting_point: Optional[str] = None
    meeting_latitude: Optional[float] = None
    meeting_longitude: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
