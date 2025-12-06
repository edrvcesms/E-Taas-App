from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from typing import List
from fastapi import HTTPException, status
from fastapi import APIRouter, Depends, Request
from dependencies.auth import current_user
from schemas.users import UserBase, UserUpdate
from models.users import User
from models.notification import Notification
from dependencies.database import get_db
from services.users import get_user_by_id, update_user_details, delete_user, logout_user
from services.notification import get_notifications_for_user
from dependencies.limiter import limiter

router = APIRouter()

@router.get("/details", response_model=UserBase)
@limiter.limit("20/minute")
async def get_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Get user details by user ID. Requires authentication."""

    if not current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's details"
        )

    return await get_user_by_id(db, current_user.id)

@router.get("/notifications", status_code=status.HTTP_200_OK)
@limiter.limit("15/minute")
async def get_user_notifications(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Get notifications for the current user."""
    if not current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access notifications"
        )
    if current_user.is_seller:
        return await get_notifications_for_user(db, current_user.id, seller_id=current_user.seller.id)
    
    return await get_notifications_for_user(db, current_user.id)

@router.put("/update-details", response_model=UserBase)
@limiter.limit("10/minute")
async def update_user(
    request: Request,
    user_update_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Update user details by user ID. Requires authentication."""

    if not current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's details"
        )
    
    return await update_user_details(db, current_user.id, user_update_data)


@router.post("/logout", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def logout(
    request: Request,
    current_user=Depends(current_user)
):
    """Logout the current user by invalidating their refresh token."""
    if not current_user:
        return {"message": "No user is currently logged in."}
        
    return await logout_user(request)



@router.delete("/delete", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def delete_user_account(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Delete user account by user ID. Requires authentication."""

    if current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user's account"
        )
    
    await delete_user(db, current_user.id)
    return {"detail": "User account deleted successfully"}