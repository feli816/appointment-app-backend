from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.security import get_current_tenant, get_current_user
from app.db import get_session
from app.models.service import Service
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.service import ServiceRead

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=list[ServiceRead])
def list_services(
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> list[ServiceRead]:
    query = select(Service).where(Service.tenant_id == current_tenant.id)
    return session.exec(query).all()
