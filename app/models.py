from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phoneNumber: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None, index=True)
    linkedId: Optional[int] = Field(default=None, index=True)
    linkPrecedence: str = Field(default="primary") # "primary" or "secondary"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    deletedAt: Optional[datetime] = None