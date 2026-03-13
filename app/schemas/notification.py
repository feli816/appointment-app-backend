from datetime import datetime

from sqlmodel import SQLModel


class NotificationRead(SQLModel):
    id: int
    tenant_id: int
    user_id: int
    title: str
    body: str
    is_read: bool
    created_at: datetime
