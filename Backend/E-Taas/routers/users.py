from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from fastapi import APIRouter, Depends, Request
from dependencies.auth import current_user
from schemas.users import UserBase, UserUpdate
from schemas.cart import CartItemBase
from models.users import User
from dependencies.database import get_db
import logging
from services.users import get_user_by_id, update_user_details, delete_user, logout_user
from dependencies.limiter import limiter
from services.cart import get_cart_by_user, get_cart_items, add_item_to_cart, remove_item_from_cart, clear_cart, edit_cart_item

logger = logging.getLogger(__name__)

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

@router.get("/cart", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def get_user_cart(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Get the current user's cart details."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to access cart."
        )

    cart = await get_cart_by_user(db, current_user.id)
    cart_items = await get_cart_items(db, cart.id)

    return {"cart": cart, "items": cart_items}


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


@router.post("/logout")
@limiter.limit("10/minute")
async def logout(
    request: Request,
    current_user=Depends(current_user)
):
    """Logout the current user by invalidating their refresh token."""
    if not current_user:
        return {"message": "No user is currently logged in."}
        
    return await logout_user(request)


@router.post("/cart/add-item", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def add_item_to_cart_endpoint(
    request: Request,
    item_data: CartItemBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Add an item to the current user's cart."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to add items to cart."
        )
    
    cart_item = await add_item_to_cart(db, current_user.id, item_data)
    return cart_item

@router.put("/cart/update-item/{item_id}", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def update_cart_item_endpoint(
    request: Request,
    item_id: int,
    item_data: CartItemBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Update an item in the current user's cart."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to update cart items."
        )
    
    cart_item = await edit_cart_item(db, item_id, item_data.quantity)
    return cart_item

@router.delete("/cart/remove-item/{item_id}", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def remove_item_from_cart_endpoint(
    request: Request,
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Remove an item from the current user's cart."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to remove items from cart."
        )
    
    response = await remove_item_from_cart(db, current_user.id, item_id)
    return response

@router.delete("/cart/clear", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")  
async def clear_cart_endpoint(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Clear all items from the current user's cart."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to clear cart."
        )
    
    response = await clear_cart(db, current_user.id)
    return response

@router.delete("/delete")
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