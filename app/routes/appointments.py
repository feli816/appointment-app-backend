from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.core.security import get_current_user, get_current_tenant
from app.models.appointment import Appointment
from app.models.service import Service
from app.models.user import User
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
    # Check service belongs to tenant
    service = session.get(Service, payload.service_id)
    if not service or service.tenant_id != current_tenant.id:
        raise HTTPException(status_code=404, detail="Service not found for tenant")

    # Check user belongs to tenant
    user = session.get(User, payload.user_id)
    if not user or user.tenant_id != current_tenant.id:
        raise HTTPException(status_code=404, detail="User not found for tenant")

    appointment_data = payload.dict()
    appointment_data["tenant_id"] = current_tenant.id

    appointment = Appointment(**appointment_data)
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    return appointment


@router.get("", response_model=list[AppointmentRead])
def list_appointments(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> list[AppointmentRead]:
    query = select(Appointment).where(Appointment.tenant_id == current_tenant.id)
    return session.exec(query).all()
