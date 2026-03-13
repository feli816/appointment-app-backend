from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(index=True, foreign_key="tenants.id")
    sender_id: int = Field(foreign_key="users.id", index=True)
    recipient_id: int = Field(foreign_key="users.id", index=True)
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
