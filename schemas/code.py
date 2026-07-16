from pydantic import BaseModel
from uuid import UUID 
from datetime import datetime

class Code(BaseModel):
    uuid: UUID
    is_used: bool | None = None
    timestamp: datetime | None = None