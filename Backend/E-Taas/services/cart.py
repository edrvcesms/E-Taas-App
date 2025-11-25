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
    
async def add_item_to_cart(db: AsyncSession, user_id: int, item_data: CartItemBase) -> CartItem:
    try:
        cart = await get_cart_by_user(db, user_id)
        
        result = await db.execute(
            select(Product).where(Product.id == item_data.product_id)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )
        
        price = 0.0
        if item_data.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock for the requested quantity."
            )
        
        subtotal = item_data.quantity * price
        if item_data.variant_id:
            result = await db.execute(
                select(ProductVariant).where(ProductVariant.id == item_data.variant_id, ProductVariant.product_id == item_data.product_id)
            )
            variant = result.scalar_one_or_none()
            
            if not variant:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product variant not found."
                )
            price = variant.price
            subtotal = item_data.quantity * price
        else:
            price = product.base_price
            subtotal = item_data.quantity * price

        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            variant_id=item_data.variant_id,
            quantity=item_data.quantity,
            price=price,
            subtotal=subtotal
        )
        db.add(cart_item)
        await db.commit()
        await db.refresh(cart_item)
        logger.info(f"Added item to cart: {cart_item}")
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"detail": "Item added to cart successfully.", "cart_item": {
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
            detail="Failed to add item to cart."
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

async def clear_cart(db: AsyncSession, cart_id: int) -> None:
    try:
        result = await db.execute(
            select(CartItem).where(CartItem.cart_id == cart_id)
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