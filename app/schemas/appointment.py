from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class AppointmentRead(SQLModel):
    id: int
    tenant_id: int
    service_id: Optional[int] = None
    user_id: int
    instructor_id: int
    slot_id: Optional[int] = None
    start_datetime: datetime
    end_datetime: datetime
    status: str
    meeting_point: Optional[str] = None


class AppointmentCreate(SQLModel):
    service_id: Optional[int] = None
    user_id: int
    instructor_id: int
    slot_id: Optional[int] = None
    start_datetime: datetime
    end_datetime: datetime
    status: Optional[str] = "pending"
    meeting_point: Optional[str] = None
    meeting_latitude: Optional[float] = None
    meeting_longitude: Optional[float] = None
