from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class UserType(str, Enum):
    ADMIN = "ADMIN"
    PROFESSIONAL = "PROFESSIONAL"
    CONSUMER = "CONSUMER"


class UserCreate(BaseModel):
    username: str
    name: str
    email: str
    password: str
    user_type: UserType


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str
    name: str
    email: str
    password: str
    user_type: UserType


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    user_type: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, user):
        user_type_str = user.user_type.value
        return cls(
            id=user.id,
            username=user.username,
            name=user.name,
            email=user.email,
            user_type=user_type_str,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
