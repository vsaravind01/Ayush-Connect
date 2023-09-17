from sqlalchemy import Column, String, BigInteger
from app.database import Base


class PlantID(Base):
    __tablename__ = "plant_ids"

    id = Column(BigInteger, primary_key=True, index=True)
    scientific_name = Column(String, unique=True, index=True)
