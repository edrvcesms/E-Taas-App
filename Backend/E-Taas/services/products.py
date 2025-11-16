from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from models.products import Product, VariantAttribute, VariantCategory, ProductVariant
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.product import ProductCreate, ProductUpdate, VariantCreate, VariantCategoryCreate, VariantAttributeCreate

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

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Product added successfully",
                "product_id": new_product.id
            }
        )

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
                "message": "Product updated successfully",
                "product_id": existing_product.id
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
async def add_variant_category(db: AsyncSession, category: VariantCategoryCreate) -> JSONResponse:
    try:
        new_category = VariantCategory(
            product_id=category.product_id,
            category_name=category.category_name
        )
        
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Variant category added successfully",
                "category_id": new_category.id
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
async def add_variant_attribute(db: AsyncSession, attribute: VariantAttributeCreate) -> JSONResponse:
    try:
        new_attribute = VariantAttribute(
            category_id=attribute.category_id,
            value=attribute.value
        )
        
        db.add(new_attribute)
        await db.commit()
        await db.refresh(new_attribute)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Variant attribute added successfully",
                "attribute_id": new_attribute.id
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        print("`Error:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
async def add_product_variant(db: AsyncSession, variant: VariantCreate) -> JSONResponse:
    try:

        categories_query = await db.execute(
            select(VariantCategory).where(VariantCategory.product_id == variant.product_id)
        )
        categories = categories_query.scalars().all()

        if not categories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This product has no variant categories."
            )

        attributes_query = await db.execute(
            select(VariantAttribute).where(VariantAttribute.id.in_(variant.attribute_ids))
        )
        attributes = attributes_query.scalars().all()

        if len(attributes) != len(variant.attribute_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more variant attribute IDs are invalid."
            )

        valid_category_ids = [cat.id for cat in categories]

        for attr in attributes:
            if attr.category_id not in valid_category_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Attribute '{attr.value}' does not belong to this product's categories."
                )

        variant_name = " - ".join([attr.value for attr in attributes])

        new_variant = ProductVariant(
            product_id=variant.product_id,
            stock=variant.stock,
            price=variant.price,
            image_url=variant.image_url,
            variant_name=variant_name
        )

        new_variant.attributes = attributes

        db.add(new_variant)
        await db.commit()
        await db.refresh(new_variant)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Product variant added successfully",
                "variant_id": new_variant.id
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        print("Errorssss:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
