from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models.appointment import Appointment
from app.models.service import Service
from app.models.user import User
from app.schemas.appointment import AppointmentCreate, AppointmentRead

router = APIRouter(prefix="/appointments", tags=["appointments"])


tenant_id_default = 1


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, session: Session = Depends(get_session)) -> Appointment:
    tenant_id = payload.tenant_id

    service = session.get(Service, payload.service_id)
    user = session.get(User, payload.user_id)
    if not service or service.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Service not found for tenant")
    if not user or user.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="User not found for tenant")

    appointment = Appointment(**payload.dict())
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    return appointment


@router.get("", response_model=list[AppointmentRead])
def list_appointments(session: Session = Depends(get_session)) -> list[AppointmentRead]:
    query = select(Appointment).where(Appointment.tenant_id == tenant_id_default)
    appointments = session.exec(query).all()
    return appointments
