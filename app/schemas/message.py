from datetime import datetime

from sqlmodel import SQLModel


class MessageCreate(SQLModel):
    recipient_id: int
    body: str


class MessageRead(SQLModel):
    id: int
    tenant_id: int
    sender_id: int
    recipient_id: int
    body: str
    created_at: datetime
