from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, or_, select

from app.core.security import get_current_tenant, get_current_user
from app.db import get_session
from app.models.message import Message
from app.models.notification import Notification
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.message import MessageCreate, MessageRead

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
def send_message(
    payload: MessageCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> Message:
    recipient = session.get(User, payload.recipient_id)
    if not recipient or recipient.tenant_id != current_tenant.id:
        raise HTTPException(status_code=404, detail="Recipient not found")

    msg = Message(
        tenant_id=current_tenant.id,
        sender_id=current_user.id,
        recipient_id=payload.recipient_id,
        body=payload.body,
    )
    session.add(msg)
    session.add(
        Notification(
            tenant_id=current_tenant.id,
            user_id=recipient.id,
            title="Nouveau message",
            body=f"Message de {current_user.name}",
        )
    )
    session.commit()
    session.refresh(msg)
    return msg


@router.get("", response_model=list[MessageRead])
def list_messages(
    peer_user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> list[Message]:
    peer = session.get(User, peer_user_id)
    if not peer or peer.tenant_id != current_tenant.id:
        raise HTTPException(status_code=404, detail="User not found")

    query = select(Message).where(
        Message.tenant_id == current_tenant.id,
        or_(
            (Message.sender_id == current_user.id) & (Message.recipient_id == peer_user_id),
            (Message.sender_id == peer_user_id) & (Message.recipient_id == current_user.id),
        ),
    )
    return session.exec(query).all()
