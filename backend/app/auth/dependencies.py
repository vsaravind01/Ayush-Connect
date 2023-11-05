#Standard Imports
import os

#Third Party Imports
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from dotenv import load_dotenv

#Fastapi imports
from fastapi import  Cookie, Depends, status
from fastapi.exceptions import HTTPException

#Ayush-Connect imports
from app.auth.models import User
from app.auth.schemas import UserResponse, UserType
from app.index.dependencies import get_db

load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']

def get_current_user(access_token: str = Cookie(None), db = Depends(get_db)):
    if access_token is None:
        return None
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def is_admin(user: UserResponse = Depends(get_current_user)):
    if user and user.user_type.value == UserType.ADMIN.value:
        return True
    return False


def is_professional(user: UserResponse = Depends(get_current_user)):
    if user and user.user_type.value == UserType.PROFESSIONAL.value:
        return True
    return False


def is_consumer(user: UserResponse = Depends(get_current_user)):
    if user and user.user_type.value == UserType.CONSUMER.value:
        return True
    return False
