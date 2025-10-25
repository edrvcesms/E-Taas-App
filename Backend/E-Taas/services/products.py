from core.cloudinary import cloudinary
import cloudinary.uploader
from schemas.product import ProductCreate
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Product, Variant, VariantCategory, ProductImage
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

async def create_new_product(
    db: AsyncSession,
    product_data: ProductCreate,
    user_id: int
) -> Product:
    
    try:
        product = Product(
            name=product_data.name,
            description=product_data.description,
            base_price=product_data.base_price,
            seller_id=user_id,
            category_id=product_data.category_id
        )

        db.add(product)
        await db.commit()
        await db.refresh(product)
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create product")
    
    if product_data.images:
        for image_url in product_data.images:
            try:
                upload_result = cloudinary.uploader.upload(image_url)
                product_image = ProductImage(
                    product_id=product.id,
                    image_url=upload_result.get("secure_url")
                )
                db.add(product_image)
            except Exception as e:
                logger.error(f"Error uploading product image: {e}")
        await db.commit()

    if product_data.variants:
        for variant_data in product_data.variants:
            try:
                variant = Variant(
                    product_id=product.id,
                    variant_combination=variant_data.variant_combination,
                    price=variant_data.variant_price,
                    stock_quantity=variant_data.stock_quantity
                )
                db.add(variant)
                await db.commit()
                await db.refresh(variant)

                if variant_data.image:
                    upload_result = cloudinary.uploader.upload(variant_data.image)
                    variant_image = ProductImage(
                        product_id=product.id,
                        image_url=upload_result.get("secure_url")
                    )
                    db.add(variant_image)
                    await db.commit()
            except Exception as e:
                logger.error(f"Error creating variant or uploading variant image: {e}")
                await db.rollback()

    return product

