#Third Party Imports
import bcrypt  
from passlib.context import CryptContext  

#Fastapi imports
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

#Ayush-Connect imports
from app.auth.models import User
from app.auth.schemas import UserCreate, UserUpdate, UserResponse
from app.index.dependencies import get_db


router = APIRouter(prefix="/users", tags=["users"])

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/")
async def create_user(user: UserCreate, db = Depends(get_db)) -> JSONResponse:
    """
    Create a new user in the database.

    Parameters
    ----------
    - **user**: (UserCreate) User creation details
        - **username**: Username of the user
        - **name**: Name of the user
        - **email**: Email of the user
        - **password**: Password of the user
        - **user_type**: Type of user (ADMIN, PROFESSIONAL, CONSUMER)
    **db**: (Session) Database session

    Returns
    -------
    - **JSONResponse**: JSON response with the status of user creation

    Raises
    ------
    - **HTTPException**
        - **500** - If user creation fails
    """
    try:
        hashed_password = password_context.hash(user.password)
        print(hashed_password)
        db_user = User(
            username=user.username,
            name=user.name,
            email=user.email,
            password=hashed_password,
            user_type=user.user_type,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed insering into db."
        )
    return JSONResponse(
        status_code=201,
        content={
            "message": f"User - '{db_user.username}' created successfully."
        }
    )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db = Depends(get_db)):
    """
    Retrieve user information by user ID.

    Parameters
    ----------
    - **user_id**: (int) The ID of the user to retrieve.
    **db**: (Session) Database session

    Returns
    -------
    - **UserResponse**: User information in a JSON-serializable format

    Raises
    ------
    - **HTTPException**
        - **404** - If the user with the specified ID is not found
        - **500** - If there is an error while fetching user information
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        print(type(db_user.user_type))
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user from db."
        )
    return UserResponse.from_orm(db_user)


@router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db = Depends(get_db)) -> JSONResponse:
    """
    Update user information by user ID.

    Parameters
    ----------
    - **user_id**: (int) The ID of the user to update.
    - **user**: (UserUpdate) User update details
    **db**: (Session) Database session

    Returns
    -------
    - **JSONResponse**: JSON response with the status of user update

    Raises
    ------
    - **HTTPException**
        - **404** - If the user with the specified ID is not found
        - **500** - If there is an error while updating user information
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update user details."
        )
    return JSONResponse(
        status_code=201,
        content={
            "message": f"User - '{db_user.username}' updated successfully."
        }
    )


@router.delete("/{user_id}")
async def delete_user(user_id: int, db = Depends(get_db)) -> JSONResponse:
    """
    Delete a user by user ID.

    Parameters
    ----------
    - **user_id**: (int) The ID of the user to delete.
    **db**: (Session) Database session

    Returns
    -------
    - **JSONResponse**: JSON response with the status of user deletion

    Raises
    ------
    - **HTTPException**
        - **404** - If the user with the specified ID is not found
        - **500** - If there is an error while deleting user information
    """
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete user details."
        )
    return JSONResponse(
        status_code=201,
        content={
            "message": f"User - '{db_user.username}' deleted successfully."
        }
    )
    