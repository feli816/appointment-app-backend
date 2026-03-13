from datetime import datetime

from sqlmodel import SQLModel


class LessonSlotCreate(SQLModel):
    instructor_id: int
    start_datetime: datetime
    end_datetime: datetime


class LessonSlotRead(SQLModel):
    id: int
    tenant_id: int
    instructor_id: int
    start_datetime: datetime
    end_datetime: datetime
    is_booked: bool
    is_active: bool
