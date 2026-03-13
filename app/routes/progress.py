from datetime import datetime

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.security import get_current_tenant, get_current_user
from app.db import get_session
from app.models.progress import StudentProgress
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.progress import ProgressRead, ProgressUpsert

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("", response_model=ProgressRead)
def upsert_progress(
    payload: ProgressUpsert,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> StudentProgress:
    existing = session.exec(
        select(StudentProgress).where(
            StudentProgress.tenant_id == current_tenant.id,
            StudentProgress.student_id == payload.student_id,
            StudentProgress.skill_code == payload.skill_code,
        )
    ).first()

    if existing:
        existing.validated = payload.validated
        existing.note = payload.note
        existing.instructor_id = current_user.id
        existing.updated_at = datetime.utcnow()
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing

    progress = StudentProgress(
        tenant_id=current_tenant.id,
        student_id=payload.student_id,
        instructor_id=current_user.id,
        skill_code=payload.skill_code,
        validated=payload.validated,
        note=payload.note,
    )
    session.add(progress)
    session.commit()
    session.refresh(progress)
    return progress


@router.get("/{student_id}", response_model=list[ProgressRead])
def list_progress(
    student_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> list[StudentProgress]:
    query = select(StudentProgress).where(
        StudentProgress.tenant_id == current_tenant.id,
        StudentProgress.student_id == student_id,
    )
    return session.exec(query).all()
