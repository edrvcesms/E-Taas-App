from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.database import get_db
from dependencies.auth import current_user
from dependencies.limiter import limiter
from services.cart import get_cart_by_user, get_cart_items, add_item_to_cart, remove_item_from_cart, clear_cart, edit_cart_item
from models.users import User
from schemas.cart import CartItemBase

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
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


@router.post("/add-item", status_code=status.HTTP_201_CREATED)
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

@router.put("/update-item/{item_id}", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def update_cart_item_endpoint(
    request: Request,
    item_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Update an item in the current user's cart."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to update cart items."
        )
    
    cart_item = await edit_cart_item(db, item_id, quantity)
    return cart_item

@router.delete("/remove-item/{item_id}", status_code=status.HTTP_200_OK)
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

@router.delete("/clear", status_code=status.HTTP_200_OK)
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
