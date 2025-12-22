from typing import List, Optional
from fastapi import HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
from app.models.products import Product, VariantAttribute, VariantCategory, ProductVariant, variant_attribute_values, ProductImage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.schemas.product import ProductCreate, VariantCreate, VariantCategoryCreate, UpdateVariantCategory, UpdateProduct
from collections import defaultdict
from itertools import product
from sqlalchemy.orm import selectinload
import json
from app.utils.cloudinary import upload_image_to_cloudinary
from app.utils.logger import logger

async def get_all_products(db: AsyncSession):
    try: 
        result = await db.execute(select(Product).options(selectinload(Product.variants)).options(selectinload(Product.images)).options(selectinload(Product.category)).options(selectinload(Product.seller)))
        products = result.scalars().all()
        logger.info(f"Retrieved all products: {products}")
        return products
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error retrieving all products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching products."
        )
    

async def get_products_by_seller(db: AsyncSession, seller_id: int):
    try:
        result = await db.execute(select(Product).options(selectinload(Product.variants)).options(selectinload(Product.images)).options(selectinload(Product.category)).options(selectinload(Product.seller)).where(Product.seller_id == seller_id))
        products = result.scalars().all()
        logger.info(f"Retrieved products for seller_id {seller_id}: {products}")
        return products

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error retrieving products for seller_id {seller_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching products for the seller."
        )

async def get_product_by_id(db: AsyncSession, product_id: int):
    try:
        result = await db.execute(select(Product).options(selectinload(Product.variants)).options(selectinload(Product.images)).options(selectinload(Product.category)).options(selectinload(Product.seller)).where(Product.id == product_id))
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
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error retrieving product by id {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the product."
        )

async def get_variants_by_product_id(db: AsyncSession, product_id: int):
    try:
        result = await db.execute(select(ProductVariant).where(ProductVariant.product_id == product_id))
        variants = result.scalars().all()
        logger.info(f"Retrieved variants for product_id {product_id}: {variants}")
        return variants
    except Exception as e:
        logger.error(f"Error retrieving variants for product_id {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the product variants."
        )

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
        logger.info(f"Created new product: {new_product}")

        return new_product

    except HTTPException:
        logger.error(f"HTTPException while adding product for seller_id {seller_id}")
        raise

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
async def add_product_images(db: AsyncSession, product_id: int, images: List[UploadFile]) -> JSONResponse:
    try:
        result = await db.execute(select(ProductImage).where(ProductImage.product_id == product_id))
        product_images = result.scalars().all()

        if not product_images:
            product_images = []
            

        if len(product_images) + len(images) > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A product can have a maximum of 10 images."
            )

        for image in images:
            upload_result = await upload_image_to_cloudinary([image], folder="product_images")
            new_image = ProductImage(
                product_id=product_id,
                image_url=upload_result[0]["secure_url"]
            )
            db.add(new_image)
            product_images.append(new_image)
            logger.info(f"Added product image: {new_image.image_url} for product_id {product_id}")
        await db.commit()
        return product_images
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error adding product images for product_id {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding product images."
        )


async def update_product_service(db: AsyncSession, product_id: int, product_update: UpdateProduct) -> JSONResponse:
    try:
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
        logger.info(f"Updated product_id {product_id}: {product}")
        
        return product
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error updating product_id {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the product."
        )


    
async def add_variant_categories_with_attributes(db: AsyncSession, categories: List[VariantCategoryCreate], product_id: int):
    try:
        created_categories = []
        for cat_data in categories:
            new_cat = VariantCategory(
                category_name=cat_data.category_name,
                product_id=product_id
            )
            db.add(new_cat)
            await db.commit()
            await db.refresh(new_cat)
            logger.info(f"Added variant category: {new_cat.category_name} for product_id {product_id}")
            if cat_data.attributes:
                for attr_data in cat_data.attributes:
                    new_attr = VariantAttribute(
                        value=attr_data.value,
                        category_id=new_cat.id
                    )
                    db.add(new_attr)
                    logger.info(f"Added variant attribute: {new_attr.value} for category_id {new_cat.id}")
                await db.commit()
            created_categories.append(new_cat)
        return created_categories
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error adding variant categories for product_id {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding variant categories."
        )

async def add_product_variants(db: AsyncSession, variants: Optional[List[VariantCreate]], product_id: int):
    try:
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
        for variant in variants:
            for combo in variant_combinations:

                variant_name = " - ".join([attr.value for attr in combo])
                new_variant = ProductVariant(
                    product_id=product_id,
                    variant_name=variant_name,
                    stock=variant.stock if variant.stock is not None else 0,
                    price=variant.price if variant.price is not None else 0.0,
                    image_url=""
                )
                db.add(new_variant)
                await db.commit()
                await db.refresh(new_variant)

                link_rows = []
                for attr in combo:
                    link_rows.append({
                        "variant_id": new_variant.id,
                        "attribute_id": attr.id
                    })
                await db.execute(variant_attribute_values.insert(), link_rows)
                created_variants.append(new_variant)

        await db.commit()
        return created_variants
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error adding product variants for product_id {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding product variants."
        )


async def update_variants(db: AsyncSession, files, variant_ids, variant_data):
    try:
        variant_ids_list = json.loads(variant_ids)
        variant_data_list = json.loads(variant_data)

        file_map = {}
        for file, variant_id in zip(files, variant_ids_list):
            file_map[variant_id] = file
        
        logger.info(f"Updating variants with IDs: {variant_ids_list}")

        results = []

        for variant_info in variant_data_list:
            variant_id = variant_info["variant_id"]

            query = await db.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
            variant = query.scalar_one_or_none()
            if not variant:
                continue

            new_image_url = variant.image_url
            if variant_info.get("remove_image"):

                new_image_url = ""
                # implement later to delete from cloudinary
                logger.info(f"Removed image for variant_id {variant_id}")

            elif variant_id in file_map:

                upload_result = await upload_image_to_cloudinary([file_map[variant_id]], folder="product-variants")
                new_image_url = upload_result[0]["secure_url"]
                logger.info(f"Updated image for variant_id {variant_id}: {new_image_url}")

            await db.execute(
                update(ProductVariant)
                .where(ProductVariant.id == variant_id)
                .values(
                    price=variant_info.get("price", variant.price),
                    stock=variant_info.get("stock", variant.stock),
                    image_url=new_image_url
                )
            )
            logger.info(f"Updated variant_id {variant_id} with price: {variant_info.get('price', variant.price)}, stock: {variant_info.get('stock', variant.stock)}")

            results.append({
                "variant_id": variant_id,
                "price": variant_info.get("price", variant.price),
                "stock": variant_info.get("stock", variant.stock),
                "image_url": new_image_url
            })

        await db.commit()
        return {"message": f"Updated {len(results)} variants", "results": results}
    

    except Exception as e:
        logger.error(f"Error in bulk updating variants: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def update_variant_category_service(db: AsyncSession, category_update: UpdateVariantCategory):
    try:
        result = await db.execute(
            select(VariantCategory).where(VariantCategory.id == category_update.id)
        )
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=404, detail="Variant category not found.")

        original_attrs_result = await db.execute(
            select(VariantAttribute).where(VariantAttribute.category_id == category.id)
        )
        original_attrs = original_attrs_result.scalars().all()
        original_attr_map = {attr.id: attr.value for attr in original_attrs}

        if category_update.category_name is not None:
            category.category_name = category_update.category_name
            db.add(category)
        

        attributes_changed = False
        logger.info(f"Original attributes: {original_attr_map}")
        logger.info(f"Update attributes: {[{'id': getattr(item, 'id', None), 'value': item.value} for item in (category_update.attributes or [])]}")
        logger.info(f"Attributes changed: {attributes_changed}")
        new_attr_ids = set()

        if category_update.attributes is not None:
            # Get current attributes again after potential changes
            current_attrs_result = await db.execute(
                select(VariantAttribute).where(VariantAttribute.category_id == category.id)
            )
            current_attrs = current_attrs_result.scalars().all()
            existing_map = {attr.id: attr for attr in current_attrs}

            # Check for changes
            for item in category_update.attributes:
                attr_id = getattr(item, "id", None)
                if attr_id in existing_map:
                    # Existing attribute - check if value changed
                    if existing_map[attr_id].value != item.value:
                        attributes_changed = True
                        existing_map[attr_id].value = item.value
                        db.add(existing_map[attr_id])
                    new_attr_ids.add(attr_id)
                    del existing_map[attr_id]
                else:
                    # New attribute
                    attributes_changed = True
                    new_attr = VariantAttribute(
                        value=item.value,
                        category_id=category.id
                    )
                    db.add(new_attr)

            # Check if any attributes were deleted
            if existing_map:
                attributes_changed = True
                for leftover in existing_map.values():
                    await db.delete(leftover)

        await db.flush()

        # Only proceed with variant regeneration if attributes actually changed
        if attributes_changed:
            print("Attributes changed - regenerating variants")
            # Your existing variant regeneration logic here
            cats = await db.execute(
                select(VariantCategory).where(VariantCategory.product_id == category.product_id)
            )
            all_categories = cats.scalars().all()
            
            attrs = await db.execute(
                select(VariantAttribute).where(
                    VariantAttribute.category_id.in_([c.id for c in all_categories])
                )
            )
            all_attrs = attrs.scalars().all()
            
            groups = defaultdict(list)
            for a in all_attrs:
                groups[a.category_id].append(a)
            
            sorted_groups = [groups[categ.id] for categ in all_categories]
            combos = list(product(*sorted_groups))
            combo_sets = {tuple(sorted(a.id for a in combo)): combo for combo in combos}

            # Get existing variants and their attribute mappings
            variant_rows = await db.execute(
                select(ProductVariant).where(ProductVariant.product_id == category.product_id)
            )
            variants = variant_rows.scalars().all()
            variant_ids = [variant.id for variant in variants]
            
            link_rows = await db.execute(
                select(variant_attribute_values).where(
                    variant_attribute_values.c.variant_id.in_(variant_ids)
                )
            )
            link_data = link_rows.mappings().all()
            
            variant_map = defaultdict(list)
            for row in link_data:
                variant_map[row["variant_id"]].append(row["attribute_id"])
            
            existing_sets = {
                v.id: tuple(sorted(variant_map[v.id])) for v in variants
            }
            
            matched = set()
            for v in variants:
                vid = v.id
                aset = existing_sets[vid]
                if aset in combo_sets:
                    combo = combo_sets[aset]
                    v.variant_name = " - ".join(a.value for a in combo)
                    db.add(v)
                    # Only update the links if they changed
                    current_links = set(variant_map[vid])
                    new_links = set(a.id for a in combo)
                    if current_links != new_links:
                        await db.execute(
                            variant_attribute_values.delete().where(
                                variant_attribute_values.c.variant_id == v.id
                            )
                        )
                        rows = [{"variant_id": v.id, "attribute_id": a.id} for a in combo]
                        await db.execute(variant_attribute_values.insert(), rows)
                    matched.add(aset)
                else:
                    # Only delete if this variant combo no longer exists
                    await db.execute(
                        variant_attribute_values.delete().where(
                            variant_attribute_values.c.variant_id == v.id
                        )
                    )
                    await db.delete(v)
            
            # Only create new variants for combinations that don't exist
            for aset, combo in combo_sets.items():
                if aset not in matched:
                    new_variant = ProductVariant(
                        product_id=category.product_id,
                        stock=0,
                        price=0.0,
                        image_url="",
                        variant_name=" - ".join(a.value for a in combo)
                    )
                    db.add(new_variant)
                    await db.flush()
                    rows = [{"variant_id": new_variant.id, "attribute_id": a.id} for a in combo]
                    await db.execute(variant_attribute_values.insert(), rows)
        else:
            logger.info("No attribute changes detected - skipping variant regeneration")

        await db.commit()
        await db.refresh(category)
        return category
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error updating variant category_id {category_update.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the variant category."
        )


async def delete_product_service(db: AsyncSession, product_id: int) -> JSONResponse:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    
    await db.delete(product)
    await db.commit()
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Product deleted successfully."}
    )
