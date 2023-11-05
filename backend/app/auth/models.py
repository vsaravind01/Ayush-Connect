from datetime import datetime
from enum import Enum as UserEnum

from sqlalchemy import Column, DateTime, Enum, Integer, String

from app.database import Base


class UserType(UserEnum):
    ADMIN = "ADMIN"
    PROFESSIONAL = "PROFESSIONAL"
    CONSUMER = "CONSUMER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )
