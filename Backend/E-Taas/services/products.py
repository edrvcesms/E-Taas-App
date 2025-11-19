from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from models.products import Product, VariantAttribute, VariantCategory, ProductVariant, variant_attribute_values
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.product import ProductCreate, ProductFullCreate, VariantCreate, VariantCategoryCreate, UpdateVariantCategory, UpdateProduct, VariantUpdate
from collections import defaultdict
from itertools import product

async def get_all_products(db: AsyncSession):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products

async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    if product.has_variants:
        variants = await get_variants_by_product_id(db, product_id)
    
    return {
        "product": product,
        "variants": variants if product.has_variants else []
    }

async def get_variants_by_product_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(ProductVariant).where(ProductVariant.product_id == product_id))
    variants = result.scalars().all()
    return variants

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
    
    
async def update_product_service(db: AsyncSession, product_id: int, product_update: UpdateProduct) -> JSONResponse:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    
    for var, value in vars(product_update).items():
        if value is not None:
            setattr(product, var, value)
    
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return product


    
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


async def update_variant_category_service(db: AsyncSession, category_update: UpdateVariantCategory):
    result = await db.execute(
        select(VariantCategory).where(VariantCategory.id == category_update.id)
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Variant category not found.")

    if category_update.category_name is not None:
        category.category_name = category_update.category_name
        db.add(category)

    if category_update.attributes is not None:
        q = await db.execute(
            select(VariantAttribute).where(VariantAttribute.category_id == category.id)
        )
        existing_attr = q.scalars().all()
        existing_map = {attr.id: attr for attr in existing_attr}

        for item in category_update.attributes:
            if getattr(item, "id", None) in existing_map:
                attr = existing_map[item.id]
                attr.value = item.value
                db.add(attr)
                del existing_map[item.id]
            else:
                new_attr = VariantAttribute(
                    value=item.value,
                    category_id=category.id
                )
                db.add(new_attr)

        for leftover in existing_map.values():
            await db.delete(leftover)

    await db.flush()

    category_rows = await db.execute(
        select(VariantCategory).where(VariantCategory.product_id == category.product_id)
    )
    all_categories = category_rows.scalars().all()

    attr_rows = await db.execute(
        select(VariantAttribute).where(
            VariantAttribute.category_id.in_([c.id for c in all_categories])
        )
    )
    all_attributes = attr_rows.scalars().all()

    groups = defaultdict(list)
    for attr in all_attributes:
        groups[attr.category_id].append(attr)

    sorted_groups = [groups[c.id] for c in all_categories]
    combos = list(product(*sorted_groups))

    variant_rows = await db.execute(
        select(ProductVariant).where(ProductVariant.product_id == category.product_id)
    )
    variants = variant_rows.scalars().all()

    await db.execute(
        variant_attribute_values.delete().where(
            variant_attribute_values.c.variant_id.in_([v.id for v in variants])
        )
    )

    for variant, combo in zip(variants, combos):
        variant.variant_name = " - ".join([a.value for a in combo])
        db.add(variant)

        rows = [{"variant_id": variant.id, "attribute_id": a.id} for a in combo]
        await db.execute(variant_attribute_values.insert(), rows)

    await db.commit()
    await db.refresh(category)
    return category


async def update_variant_service(db: AsyncSession, variant_id: int, variant_update: VariantUpdate) -> JSONResponse:
    result = await db.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
    variant = result.scalar_one_or_none()
    if not variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant not found."
        )
    
    for var, value in vars(variant_update).items():
        if value is not None:
            setattr(variant, var, value)
    
    db.add(variant)
    await db.commit()
    await db.refresh(variant)
    
    return variant
