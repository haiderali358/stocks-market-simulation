from sqlalchemy import Column, Integer, Boolean, DateTime
from datetime import datetime
from database.database import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow
    )

