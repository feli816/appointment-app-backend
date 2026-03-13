from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.security import get_current_tenant, get_current_user
from app.db import get_session
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> User:
    if payload.tenant_id != current_tenant.id:
        raise HTTPException(status_code=403, detail="Cannot create user outside current tenant")

    user = User(**payload.dict())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("", response_model=list[UserRead])
def list_users(
    role: str | None = None,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
) -> list[User]:
    query = select(User).where(User.tenant_id == current_tenant.id)
    if role:
        query = query.where(User.role == role)
    return session.exec(query).all()
