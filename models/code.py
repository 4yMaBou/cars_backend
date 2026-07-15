import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Code(Base):
    __tablename__ = "codes"
    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    datetime: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)