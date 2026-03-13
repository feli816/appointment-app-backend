from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.security import get_current_user, get_current_tenant
from app.db import get_session
from app.models.appointment import Appointment
from app.models.lesson_slot import LessonSlot
from app.models.notification import Notification
from app.models.service import Service
from app.models.user import User, UserRole
from app.models.tenant import Tenant
from app.schemas.appointment import AppointmentCreate, AppointmentRead

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> Appointment:
    if payload.service_id:
        service = session.get(Service, payload.service_id)
        if not service or service.tenant_id != current_tenant.id:
            raise HTTPException(status_code=404, detail="Service not found for tenant")

    student = session.get(User, payload.user_id)
    if not student or student.tenant_id != current_tenant.id:
        raise HTTPException(status_code=404, detail="Student not found for tenant")

    instructor = session.get(User, payload.instructor_id)
    if not instructor or instructor.tenant_id != current_tenant.id or instructor.role != UserRole.instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    if payload.slot_id:
        slot = session.get(LessonSlot, payload.slot_id)
        if not slot or slot.tenant_id != current_tenant.id or slot.instructor_id != payload.instructor_id:
            raise HTTPException(status_code=404, detail="Slot not found")
        if slot.is_booked or not slot.is_active:
            raise HTTPException(status_code=409, detail="Slot already booked")
        if slot.start_datetime != payload.start_datetime or slot.end_datetime != payload.end_datetime:
            raise HTTPException(status_code=400, detail="Appointment time must match selected slot")
    else:
        slot = None

    student_conflict = session.exec(
        select(Appointment).where(
            Appointment.tenant_id == current_tenant.id,
            Appointment.user_id == payload.user_id,
            Appointment.start_datetime < payload.end_datetime,
            Appointment.end_datetime > payload.start_datetime,
            Appointment.status != "cancelled",
        )
    ).first()
    if student_conflict:
        raise HTTPException(status_code=409, detail="Student already has lesson at this time")

    instructor_conflict = session.exec(
        select(Appointment).where(
            Appointment.tenant_id == current_tenant.id,
            Appointment.instructor_id == payload.instructor_id,
            Appointment.start_datetime < payload.end_datetime,
            Appointment.end_datetime > payload.start_datetime,
            Appointment.status != "cancelled",
        )
    ).first()
    if instructor_conflict:
        raise HTTPException(status_code=409, detail="Instructor already has lesson at this time")

    appointment = Appointment(tenant_id=current_tenant.id, **payload.dict())
    session.add(appointment)

    if slot:
        slot.is_booked = True
        session.add(slot)

    session.add(
        Notification(
            tenant_id=current_tenant.id,
            user_id=student.id,
            title="Réservation confirmée",
            body=f"Votre leçon avec {instructor.name} est confirmée.",
        )
    )

    if current_user.id != instructor.id:
        session.add(
            Notification(
                tenant_id=current_tenant.id,
                user_id=instructor.id,
                title="Nouveau cours réservé",
                body=f"{student.name} a réservé un cours.",
            )
        )

    session.commit()
    session.refresh(appointment)
    return appointment


@router.get("", response_model=list[AppointmentRead])
def list_appointments(
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> list[AppointmentRead]:
    query = select(Appointment).where(Appointment.tenant_id == current_tenant.id)
    return session.exec(query).all()
