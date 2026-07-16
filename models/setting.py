from typing import Any
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Setting(Base):
    __tablename__ = "settings"
    
    # Ключ настройки — строка, выступает в роли Primary Key
    key: Mapped[str] = mapped_column(String(255), primary_key=True)
    
    # Значение настройки — JSON тип для гибкости данных
    value: Mapped[Any] = mapped_column(JSON, nullable=True)
