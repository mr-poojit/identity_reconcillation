from typing import Optional
from pydantic import BaseModel


class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None