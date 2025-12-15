from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from models.cart import Cart, CartItem
from models.products import Product, ProductVariant
from schemas.cart import CartItemBase
from sqlalchemy.future import select
from utils.logger import logger

async def get_cart_by_user(db: AsyncSession, user_id: int) -> Cart:

    try:
        result = await db.execute(select(Cart).where(Cart.user_id == user_id))
        cart = result.scalar_one_or_none()
        logger.info(f"Retrieved cart for user_id {user_id}: {cart}")
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            await db.commit()
            await db.refresh(cart)
        return cart
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error retrieving cart for user_id {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the cart."
        ) from e

async def get_cart_items(db: AsyncSession, cart_id: int) -> list[CartItem]:
    try:
        result = await db.execute(select(CartItem).where(CartItem.cart_id == cart_id))
        items = result.scalars().all()
        if not items:
            return []
        return items
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error retrieving cart items for cart_id {cart_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving cart items."
        ) from e
    
async def add_item_to_cart(db: AsyncSession, user_id: int, item_data: CartItemBase):
    try:
        cart = await get_cart_by_user(db, user_id)

        result = await db.execute(
            select(Product).where(Product.id == item_data.product_id)
        )
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(404, "Product not found.")

        variant = None
        if item_data.variant_id:
            result = await db.execute(
                select(ProductVariant).where(
                    ProductVariant.id == item_data.variant_id,
                    ProductVariant.product_id == item_data.product_id
                )
            )
            variant = result.scalar_one_or_none()

            if not variant:
                raise HTTPException(404, "Product variant not found.")

            price = variant.price
        else:
            price = product.base_price

        result = await db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id,
                CartItem.product_id == item_data.product_id,
                CartItem.variant_id == item_data.variant_id
            )
        )
        existing_item = result.scalar_one_or_none()

        if existing_item:
            if item_data.quantity + existing_item.quantity > (variant.stock if variant else product.stock):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient stock for the requested quantity."
                )
            new_quantity = existing_item.quantity + item_data.quantity
            existing_item.quantity = new_quantity
            existing_item.price = price
            existing_item.subtotal = price * new_quantity

            db.add(existing_item)
            await db.commit()
            await db.refresh(existing_item)

            return JSONResponse(
                status_code=200,
                content={
                    "detail": "Cart item updated.",
                    "cart_item": {
                        "id": existing_item.id,
                        "product_id": existing_item.product_id,
                        "variant_id": existing_item.variant_id,
                        "quantity": existing_item.quantity,
                        "price": existing_item.price,
                        "subtotal": existing_item.subtotal,
                    },
                },
            )

        subtotal = price * item_data.quantity

        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            variant_id=item_data.variant_id,
            quantity=item_data.quantity,
            price=price,
            subtotal=subtotal,
        )

        db.add(cart_item)
        await db.commit()
        await db.refresh(cart_item)

        return JSONResponse(
            status_code=201,
            content={
                "detail": "Item added to cart successfully.",
                "cart_item": {
                    "id": cart_item.id,
                    "product_id": cart_item.product_id,
                    "variant_id": cart_item.variant_id,
                    "quantity": cart_item.quantity,
                    "price": cart_item.price,
                    "subtotal": cart_item.subtotal,
                },
            },
        )

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.error(f"Error adding item to cart: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to add item to cart."
        ) from e

async def remove_item_from_cart(db: AsyncSession, cart_item_id: int) -> None:
    try: 
        result = await db.execute(
            select(CartItem).where(CartItem.id == cart_item_id)
        )
        cart_item = result.scalar_one_or_none()
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found."
            )
        logger.info(f"Removing item from cart: {cart_item}")
        
        await db.delete(cart_item)
        await db.commit()
        logger.info(f"Removed item from cart: {cart_item}")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Item removed from cart successfully."}
        )
    
    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove item from cart."
        ) from e

async def clear_cart(db: AsyncSession, user_id: int) -> None:
    try:
        result = await db.execute(
            select(CartItem).where(CartItem.cart.has(Cart.user_id == user_id))
        )
        items = result.scalars().all()
        
        for item in items:
            await db.delete(item)
        
        await db.commit()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Cart cleared successfully."}
        )
    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear cart."
        ) from e

async def edit_cart_item(db: AsyncSession, cart_item_id: int, quantity: int) -> CartItem:
    try:
        result = await db.execute(
            select(CartItem).where(CartItem.id == cart_item_id)
        )
        cart_item = result.scalar_one_or_none()
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found."
            )
        
        product_result = await db.execute(
            select(Product).where(Product.id == cart_item.product_id)
        )
        product = product_result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Associated product not found."
            )
        
        if quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock for the requested quantity."
            )
        
        cart_item.quantity = quantity
        cart_item.subtotal = cart_item.price * quantity
        
        db.add(cart_item)
        await db.commit()
        await db.refresh(cart_item)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Cart item updated successfully.", "cart_item": {
                "id": cart_item.id,
                "product_id": cart_item.product_id,
                "variant_id": cart_item.variant_id,
                "quantity": cart_item.quantity,
                "price": cart_item.price,
                "subtotal": cart_item.subtotal
            }}
        )
    
    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update cart item."
        ) from e