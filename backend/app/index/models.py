from sqlalchemy import Column, Text, DateTime, Integer
from datetime import datetime
from app.database import Base


class PlantIndex(Base):
    __tablename__ = "plant_idx"

    id = Column(Integer, primary_key=True, autoincrement=True)
    idx_uuid = Column(Text, unique=True, nullable=False)
    index_name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    alias = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
