from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.orders import OrderBaseCart, OrderCreateCart, OrderCreate
from services.orders import get_orders_by_user, create_new_order, get_order_by_id
from dependencies.auth import current_user
from dependencies.database import get_db
from dependencies.limiter import limiter

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def get_user_orders(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    orders = await get_orders_by_user(db, current_user.id)
    return orders

@router.get("/{order_id}", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def get_order_details(
    request: Request,
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to view order details."
        )
    
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )
    return order

@router.post("/checkout", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def checkout_order(
    request: Request,
    order: OrderCreate,
    cart_items_id: Optional[List[int]] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to create an order."
        )
    
    new_order = await create_new_order(db, order, current_user.id, cart_items_id)
    return new_order
