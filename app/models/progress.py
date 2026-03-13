from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class StudentProgress(SQLModel, table=True):
    __tablename__ = "student_progress"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(index=True, foreign_key="tenants.id")
    student_id: int = Field(index=True, foreign_key="users.id")
    instructor_id: int = Field(index=True, foreign_key="users.id")
    skill_code: str = Field(index=True)
    validated: bool = Field(default=False)
    note: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
