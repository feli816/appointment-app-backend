from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.security import get_current_tenant, get_current_user
from app.db import get_session
from app.models.lesson_slot import LessonSlot
from app.models.tenant import Tenant
from app.models.user import User, UserRole
from app.schemas.slot import LessonSlotCreate, LessonSlotRead

router = APIRouter(prefix="/slots", tags=["slots"])


@router.post("", response_model=LessonSlotRead, status_code=status.HTTP_201_CREATED)
def create_slot(
    payload: LessonSlotCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> LessonSlot:
    instructor = session.get(User, payload.instructor_id)
    if not instructor or instructor.tenant_id != current_tenant.id or instructor.role != UserRole.instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    overlap = session.exec(
        select(LessonSlot).where(
            LessonSlot.tenant_id == current_tenant.id,
            LessonSlot.instructor_id == payload.instructor_id,
            LessonSlot.start_datetime < payload.end_datetime,
            LessonSlot.end_datetime > payload.start_datetime,
            LessonSlot.is_active.is_(True),
        )
    ).first()
    if overlap:
        raise HTTPException(status_code=409, detail="Overlapping slot")

    slot = LessonSlot(tenant_id=current_tenant.id, **payload.dict())
    session.add(slot)
    session.commit()
    session.refresh(slot)
    return slot


@router.get("", response_model=list[LessonSlotRead])
def list_slots(
    instructor_id: int | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    only_available: bool = False,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> list[LessonSlot]:
    query = select(LessonSlot).where(LessonSlot.tenant_id == current_tenant.id, LessonSlot.is_active.is_(True))
    if instructor_id:
        query = query.where(LessonSlot.instructor_id == instructor_id)
    if from_date:
        query = query.where(LessonSlot.start_datetime >= from_date)
    if to_date:
        query = query.where(LessonSlot.end_datetime <= to_date)
    if only_available:
        query = query.where(LessonSlot.is_booked.is_(False))
    return session.exec(query).all()


@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(
    slot_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> None:
    slot = session.get(LessonSlot, slot_id)
    if not slot or slot.tenant_id != current_tenant.id:
        raise HTTPException(status_code=404, detail="Slot not found")
    slot.is_active = False
    session.add(slot)
    session.commit()
