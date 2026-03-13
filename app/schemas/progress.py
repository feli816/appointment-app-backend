from typing import Optional

from sqlmodel import SQLModel


class ProgressUpsert(SQLModel):
    student_id: int
    skill_code: str
    validated: bool
    note: Optional[str] = None


class ProgressRead(SQLModel):
    id: int
    tenant_id: int
    student_id: int
    instructor_id: int
    skill_code: str
    validated: bool
    note: Optional[str] = None
