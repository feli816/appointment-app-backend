from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db import get_session
from app.models.service import Service
from app.schemas.service import ServiceRead

router = APIRouter(prefix="/services", tags=["services"])


tenant_id_default = 1


@router.get("", response_model=List[ServiceRead])
def list_services(session: Session = Depends(get_session)) -> List[ServiceRead]:
    query = select(Service).where(Service.tenant_id == tenant_id_default)
    services = session.exec(query).all()
    return services
