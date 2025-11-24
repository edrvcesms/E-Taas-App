from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.orders import Order, OrderItem
from models.users import User
from models.sellers import Seller
from models.products import Product, ProductVariant
from schemas.orders import OrderCreate, OrderItemCreate


async def get_orders_by_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(Order).where(Order.user_id == user_id))
        orders = result.scalars().all()
        if not orders:
            return []
        return orders
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching orders: {str(e)}"
        )
    
