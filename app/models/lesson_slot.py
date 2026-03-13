from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class LessonSlot(SQLModel, table=True):
    __tablename__ = "lesson_slots"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(index=True, foreign_key="tenants.id")
    instructor_id: int = Field(index=True, foreign_key="users.id")
    start_datetime: datetime
    end_datetime: datetime
    is_booked: bool = Field(default=False, index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
