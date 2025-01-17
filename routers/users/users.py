from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, Depends, HTTPException
from schemas.user.user import UserResponse, Token
from schemas.user.user import UserCreate, UserResponse
from models.user.user import User
from auth.user import get_current_user, authenticate_user, create_access_token, get_password_hash
from core.database.database import Base, engine, get_db
from core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


Base.metadata.create_all(engine)

user_router = APIRouter(prefix="/hypervisor", tags=["Authentication"])

@user_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@user_router.post("/register_user", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create user
    hashed_password = get_password_hash(user.password)
    try:
        new_user = User(
            username=user.username,
            hashed_password=hashed_password,
            role=user.role,
        )
    
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        db.rollback()  # Rollback transaction in case of errors like unique constraint violations
        raise HTTPException(status_code=400, detail="Database error, please try again later")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"An unexpected error occurred: {str(e)}")


    return UserResponse(
        username=new_user.username,
        role=new_user.role
    )

@user_router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return UserResponse(
        username=current_user.username,
        role=current_user.role,
    )