from datetime import datetime
from sqlalchemy import Column, DateTime
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
