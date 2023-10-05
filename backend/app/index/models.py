from sqlalchemy import Column, Text, Uuid, DateTime, text
from datetime import datetime
from uuid import uuid4
from app.database import Base


class PlantIndex(Base):
    __tablename__ = "plant_idx"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    index_name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    alias = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
