from sqlalchemy import Column, Text, Uuid, DateTime
from datetime import datetime
from app.database import Base


class PlantIndex(Base):
    __tablename__ = "plant_ids"

    id = Column(Uuid(as_uuid=True), primary_key=True)
    index_name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    alias = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
