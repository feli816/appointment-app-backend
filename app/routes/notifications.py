from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.security import get_current_tenant, get_current_user
from app.db import get_session
from app.models.notification import Notification
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.notification import NotificationRead

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=list[NotificationRead])
def list_notifications(
    only_unread: bool = False,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> list[Notification]:
    query = select(Notification).where(
        Notification.tenant_id == current_tenant.id,
        Notification.user_id == current_user.id,
    )
    if only_unread:
        query = query.where(Notification.is_read.is_(False))
    return session.exec(query).all()
