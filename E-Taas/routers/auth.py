from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.config import settings
from models import User
from db.database import get_db
from schemas.auth import UserCreate, UserResponse, UserLogin, Token
from datetime import datetime
from core.security import hash_password, verify_password, create_access_token, is_token_valid
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed_password = hash_password(user.password)
    print("Password before hashing:", user.password)
    print("Length:", len(user.password))

    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password,
        created_at = datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)) -> Token:
    """Login a user."""
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    expires_delta = timedelta(days=7) if user.remember_me else timedelta(hours=1)
    access_token = create_access_token(
        {
            "sub": db_user.email,
            "user_id": db_user.id,
            "role": db_user.role
        },
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=int(expires_delta.total_seconds())
    )

    
