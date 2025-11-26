from ast import List
from fastapi import HTTPException, status
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models.orders import Order, OrderItem
from models.cart import Cart, CartItem
from models.products import Product, ProductVariant
from schemas.orders import OrderCreate, OrderResponse, OrderItemResponse, OrderItemCreate
from utils.reference import generate_order_code
from datetime import datetime
from utils.logger import logger


async def get_orders_by_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(Order).where(Order.user_id == user_id))
        orders = result.scalars().all()
        logger.info(f"Retrieved orders for user_id {user_id}: {orders}")
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
    
async def create_new_order(db: AsyncSession, order_data: OrderCreate, user_id: int, cart_items_id: Optional[List[int]]):
    try:

        if cart_items_id is not None:
            result = await db.execute(
                select(CartItem)
                .options(selectinload(CartItem.product), selectinload(CartItem.variant), selectinload(CartItem.cart))
                .where(
                    CartItem.id.in_(cart_items_id),
                    CartItem.cart.has(Cart.user_id == user_id)
                )
            )
            cart_items = result.scalars().all()
            if not cart_items:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No valid cart items found for checkout."
                )   
            
            items_by_seller = {}
            for item in cart_items:
                seller_id = item.product.seller_id
                if seller_id not in items_by_seller:
                    items_by_seller[seller_id] = []
                items_by_seller[seller_id].append(item)

            new_orders = []

            for seller_id, items in items_by_seller.items():
                order_items = []
                total_amount = 0.0

                for item in items:
                    product = item.product
                    variant = item.variant

                    price = variant.price if variant else product.base_price
                    total_amount += price * item.quantity

                    order_items.append(
                        OrderItemCreate(
                            product_id=item.product_id,
                            variant_id=item.variant_id,
                            quantity=item.quantity,
                            price=price
                        )
                    )
                    logger.info(f"Prepared order item for product ID {item.product_id} with quantity {item.quantity} and price {price}")
            

                order_create_data = OrderCreate(
                    seller_id=seller_id,
                    shipping_address=order_data.shipping_address,
                    payment_method=order_data.payment_method,
                    items=order_items,
                    total_amount=total_amount
                )

                new_order = await create_new_order(db, order_create_data, user_id, None)
                new_orders.append(new_order)

                logger.info(f"Created order ID {new_order.id} for seller ID {seller_id} with total amount {total_amount}")

                for item in items:
                    await db.delete(item)
                    logger.info(f"Removed cart item ID {item.id} after checkout.")
            await db.commit()
            return new_orders
        
        else:

            total_amount = 0.0
            order_items_instances = []

            for item in order_data.items:
                logger.info(f"Processing order item: {item}")
                result = await db.execute(select(Product).where(Product.id == item.product_id))
                product = result.scalar_one_or_none()
                logger.info(f"Retrieved product for order item: {product}")
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
                
                if order_data.seller_id != product.seller_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"This product does not belong to the specified seller."
                    )
                

                if item.variant_id:
                    logger.info(f"Processing variant ID {item.variant_id} for order item: {item}")
                    result = await db.execute(select(ProductVariant).where(ProductVariant.id == item.variant_id))
                    logger.info(f"Retrieved product variant for order item: {result}")
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
                logger.info(f"Added order item instance: {order_item_instance}")

                if item.variant_id:
                    if item.quantity > variant.stock:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Insufficient stock for variant ID {item.variant_id}."
                        )
                    variant.stock -= item.quantity
                    logger.info(f"Decreased stock for variant ID {variant.id} by {item.quantity}. New stock: {variant.stock}")
                else:
                    if item.quantity > product.stock:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Insufficient stock for product ID {item.product_id}."
                        )
                    product.stock -= item.quantity

                    logger.info(f"Decreased stock for product ID {product.id} by {item.quantity}. New stock: {product.stock}")

            order_code = generate_order_code()

            new_order = Order(
                user_id=user_id,
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
            await db.flush()
            logger.info(f"Created new order: {new_order}")

            for order_item in order_items_instances:
                order_item.order_id = new_order.id
                db.add(order_item)
                logger.info(f"Added order item to order: {order_item}")

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


async def get_order_by_id(db: AsyncSession, order_id: int) -> OrderResponse:
    try:
        result = await db.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items))
        )
        order = result.scalar_one_or_none()

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with ID {order_id} not found."
            )
        logger.info(f"Retrieved order with ID {order_id}: {order}")

        return OrderResponse(
            id=order.id,
            user_id=order.user_id,
            seller_id=order.seller_id,
            total_amount=order.total_amount,
            shipping_address=order.shipping_address,
            shipping_fee=order.shipping_fee,
            payment_method=order.payment_method,
            order_reference=order.order_reference,
            shipping_link=order.shipping_link,
            status=order.status,
            payment_status=order.payment_status,
            created_at=order.created_at,
            shipped_at=order.shipped_at,
            order_received_at=order.order_received_at,
            items=[
                OrderItemResponse(
                    product_id=i.product_id,
                    variant_id=i.variant_id,
                    quantity=i.quantity,
                    price=i.price
                ) for i in order.items
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the order: {str(e)}"
        )
    
async def cancel_order_by_id(db: AsyncSession, order_id: int, user_id: int) -> Order:
    try:
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found."
            )
        if order.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to cancel this order."
            )
        if order.status != "Pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending orders can be canceled."
            )
        
        order.status = "Cancelled"
        await db.commit()
        await db.refresh(order)
        logger.info(f"Order ID {order_id} cancelled.")

        return order

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.error(f"Error canceling order ID {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel the order."
        ) from e
    
async def mark_order_as_received(db: AsyncSession, order_id: int, user_id: int) -> Order:
    try:
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found."
            )
        if order.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this order."
            )
        if order.status != "Shipped":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only shipped orders can be marked as received."
            )
        
        order.status = "Delivered"
        order.order_received_at = datetime.utcnow().isoformat()
        await db.commit()
        await db.refresh(order)
        logger.info(f"Order ID {order_id} marked as received.")

        return order

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.error(f"Error marking order ID {order_id} as received: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update the order."
        ) from e