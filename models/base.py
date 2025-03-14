from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func
from datetime import datetime

class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)

Base = declarative_base(cls=CustomBase)
