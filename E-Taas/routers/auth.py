from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import JSONResponse as Response
from sqlalchemy.orm import Session
from services.auth import register_user, login_user
from db.database import get_db
from schemas.users import UserCreate, UserResponse
from schemas.auth import LoginBase, LoginResponse
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    new_user = register_user(user, db)
    return new_user


@router.post("/login", response_model=LoginResponse)
def login(user: LoginBase, db: Session = Depends(get_db)):
    """Authenticate a user and return a JWT token."""
    token_data = login_user(user, db)
    return token_data



# @router.post("/send-verification-otp")
# async def send_verification_otp(email: str):
#     """Send an OTP to the user's email for verification."""
#     otp = generate_otp()
#     subject = "Your Email Verification OTP"
#     try:
#         send_email(email, subject, otp)
#         return {"message": "OTP sent successfully"} 
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Failed to send OTP")