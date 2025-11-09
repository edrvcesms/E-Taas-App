from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.database import get_db
from dependencies.auth import current_user
from services.auth import register_user, login_user, token_refresh
from schemas.auth import UserRegister, UserLogin
from models.users import User
from dependencies.limiter import limiter


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def register(
    request: Request,
    user_register_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user. It can also accepts register from Firebase authenticated users."""
    return await register_user(db, user_register_data)

@router.post("/login")
@limiter.limit("10/minute")
async def login(
    request: Request,
    user_login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login a user and return access and refresh tokens. It also supports Firebase authenticated users."""
    return await login_user(db, user_login_data)

@router.post("/token/refresh")
@limiter.limit("15/minute")
async def refresh_token(
    request: Request
):
    """Refresh access token using a valid refresh token."""
    return await token_refresh(request)