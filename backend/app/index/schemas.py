from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class PlantIndexBase(BaseModel):
    index_name: str
    description: str


class PlantIndexCreate(PlantIndexBase):
    pass


class PlantIndexUpdate(PlantIndexBase):
    description: Optional[str]
    alias: Optional[str]


class PlantIndexInDB(PlantIndexBase):
    id: UUID
    alias: str
    created_at: datetime
    updated_at: datetime


class PlantIndex(PlantIndexInDB):
    pass
