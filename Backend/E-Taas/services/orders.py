from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.orders import Order, OrderItem
from models.products import Product, ProductVariant
from schemas.orders import OrderCreate, OrderItemCreate
from utils.reference import generate_order_code
from datetime import datetime


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
    
async def create_new_order(db: AsyncSession, order_data: OrderCreate) -> Order:
    try:
        total_amount = 0.0
        order_items_instances = []

        for item in order_data.order_items:
            result = await db.execute(select(Product).where(Product.id == item.product_id))
            product = result.scalar_one_or_none()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {item.product_id} not found."
                )
            if item.quantity > product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product ID {item.product_id}."
                )

            # Determine price
            if item.variant_id:
                result = await db.execute(select(ProductVariant).where(ProductVariant.id == item.variant_id))
                variant = result.scalar_one_or_none()
                if not variant:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product variant with ID {item.variant_id} not found."
                    )
                price = variant.price
            else:
                price = product.base_price

            total_price = price * item.quantity
            total_amount += total_price

            order_item_instance = OrderItem(
                product_id=item.product_id,
                variant_id=item.variant_id,
                quantity=item.quantity,
                price=price,
            )
            order_items_instances.append(order_item_instance)

        # Generate order reference
        order_code = generate_order_code()

        new_order = Order(
            user_id=order_data.user_id,
            seller_id=order_data.seller_id,
            total_amount=total_amount,
            shipping_address=order_data.shipping_address,
            status="Pending",
            payment_status="Unpaid",
            payment_method=order_data.payment_method,
            order_reference=order_code,
            shipping_fee=70.0,
            created_at=datetime.utcnow().isoformat()
        )

        db.add(new_order)
        await db.flush()  # ensure new_order.id is available

        # Add all order items
        for order_item in order_items_instances:
            order_item.order_id = new_order.id
            db.add(order_item)

        await db.commit()
        await db.refresh(new_order)
        return new_order

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the order: {str(e)}"
        )
