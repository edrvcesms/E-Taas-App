from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.database import get_db
from services.auth import refresh_token_for_mobile, register_user, login_user, token_refresh, verify_email_otp, reset_password, forgot_password, verify_password_reset_otp
from schemas.auth import UserRegister, UserLogin, VerifyEmailOTP, VerifyResetPasswordOTP, PasswordReset, ForgotPasswordRequest
from dependencies.limiter import limiter


router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def register(
    request: Request,
    user_register_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    return await register_user(db, user_register_data)

@router.post("/verify-email-otp", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def verify_email_otp_endpoint(
    request: Request,
    verify_data: VerifyEmailOTP,
    db: AsyncSession = Depends(get_db)
):
    return await verify_email_otp(db, verify_data)

@router.post("/login")
@limiter.limit("10/minute")
async def login(
    request: Request,
    user_login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login a user and return access and refresh tokens. It also supports Firebase authenticated users."""
    return await login_user(db, user_login_data)

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def forgot_password_endpoint(
    request: Request,
    email: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """Initiate the password reset process by sending an OTP to the user's email."""
    return await forgot_password(db, email)

@router.post("/verify-password-reset-otp", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def verify_password_reset_otp_endpoint(
    request: Request,
    verify_data: VerifyResetPasswordOTP,
    db: AsyncSession = Depends(get_db)
):
    """Verify the OTP sent to the user's email for password reset."""
    return await verify_password_reset_otp(db, verify_data)

@router.post("/reset-password", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def reset_password_endpoint(
    request: Request,
    data: PasswordReset,
    db: AsyncSession = Depends(get_db)
):
    """Reset the user's password after OTP verification."""
    return await reset_password(db, data.email, data.new_password)

@router.post("/token/refresh")
@limiter.limit("15/minute")
async def refresh_token(
    request: Request
):
    """Refresh access token using a valid refresh token."""
    return await token_refresh(request)

@router.post("/token-refresh-mobile")
@limiter.limit("15/minute")
async def refresh_token_mobile(
    request: Request,
    token: str
):
    """Refresh access token using a valid refresh token for mobile clients."""
    return await refresh_token_for_mobile(token)