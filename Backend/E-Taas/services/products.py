from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from models.products import Product, VariantAttribute, VariantCategory, ProductVariant, variant_attribute_values
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.product import ProductCreate, ProductUpdate, VariantCreate, VariantCategoryCreate, VariantAttributeCreate
from collections import defaultdict
from itertools import product

async def add_product_service(db: AsyncSession, product: ProductCreate, seller_id: int) -> JSONResponse:
    try:
        new_product = Product(
            product_name=product.product_name,
            description=product.description,
            base_price=product.base_price,
            stock=product.stock,
            has_variants=product.has_variants,
            category_id=product.category_id,
            seller_id=seller_id
        )
        
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)

        return new_product

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
async def update_product(db: AsyncSession, product_id: int, product_data: ProductUpdate) -> JSONResponse:
    try:
        result = await db.execute(select(Product).where(Product.id == product_id))
        existing_product = result.scalar_one_or_none()

        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )

        for var, value in vars(product_data).items():
            if value is not None:
                setattr(existing_product, var, value)

        db.add(existing_product)
        await db.commit()
        await db.refresh(existing_product)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Product updated successfully"
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
async def add_variant_categories_with_attributes(db: AsyncSession, categories: list[VariantCategoryCreate], product_id: int):
    created_categories = []
    for cat_data in categories:
        new_cat = VariantCategory(
            category_name=cat_data.category_name,
            product_id=product_id
        )
        db.add(new_cat)
        await db.commit()
        await db.refresh(new_cat)
        if cat_data.attributes:
            for attr_data in cat_data.attributes:
                new_attr = VariantAttribute(
                    value=attr_data.value,
                    category_id=new_cat.id
                )
                db.add(new_attr)
            await db.commit()
        created_categories.append(new_cat)
    return created_categories

async def add_product_variants(db: AsyncSession, variants: list[VariantCreate], product_id: int):
    categories_query = await db.execute(
        select(VariantCategory).where(VariantCategory.product_id == product_id)
    )
    categories = categories_query.scalars().all()
    if not categories:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product has no variant categories.")

    attributes_query = await db.execute(
        select(VariantAttribute).where(VariantAttribute.category_id.in_([c.id for c in categories]))
    )
    attributes = attributes_query.scalars().all()
    category_attributes = defaultdict(list)
    for attr in attributes:
        category_attributes[attr.category_id].append(attr)
    attribute_groups = list(category_attributes.values())
    variant_combinations = list(product(*attribute_groups))

    created_variants = []
    for variant_data in variants:
        for combination in variant_combinations:
            variant_name = " - ".join([attr.value for attr in combination])
            new_variant = ProductVariant(
                product_id=product_id,
                stock=variant_data.stock,
                price=variant_data.price,
                image_url=variant_data.image_url,
                variant_name=variant_name
            )
            db.add(new_variant)
            await db.flush()
            await db.execute(
                variant_attribute_values.insert(),
                [{"variant_id": new_variant.id, "attribute_id": attr.id} for attr in combination]
            )
            created_variants.append(new_variant)
    await db.commit()
    return created_variants
