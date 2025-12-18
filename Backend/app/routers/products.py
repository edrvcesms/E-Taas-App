from typing import List, Optional
from fastapi import HTTPException, status, APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.products import get_product_by_id, get_all_products, add_product_service, add_product_images, update_product_service, add_variant_categories_with_attributes, add_product_variants, update_variant_category_service, update_variant_service, delete_product_service, add_image_to_single_variant
from fastapi import Form, File, UploadFile
from app.models.users import User
from app.dependencies.database import get_db
from app.dependencies.auth import current_user
from app.dependencies.limiter import limiter
from app.schemas.product import ProductFullCreate, ProductFullUpdate, VariantUpdate

router = APIRouter()

@router.get("/")
@limiter.limit("20/minute")
async def get_products(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    
  return await get_all_products(db)

@router.get("/{product_id}")
@limiter.limit("30/minute")
async def get_product(
    request: Request,
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_product_by_id(db, product_id)


@router.post("/add-variant-image/{variant_id}", status_code=status.HTTP_201_CREATED)
async def add_variant_image(
    request: Request,
    variant_id: int,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can add variant images."
        )

    return await add_image_to_single_variant(db, variant_id, image)



@router.post("/add-images/{product_id}", status_code=status.HTTP_201_CREATED)
async def add_images_to_product(
    request: Request,
    product_id: int,
    images: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can add product images."
        )

    return await add_product_images(db, product_id, images)

@router.post("/add-product", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def add_product_route(
    request: Request,
    data: ProductFullCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can add products."
        )

    product = await add_product_service(db, data.product, current_user.seller.id)

    if data.product.has_variants:
        if not data.variant_categories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Variant categories are required."
            )

        await add_variant_categories_with_attributes(db, data.variant_categories, product.id)

        variants = await add_product_variants(db, data.variants, product.id)

    return {"product": product, "variants": variants if data.product.has_variants else []}



@router.put("/update-product/{product_id}", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def update_product(
    request: Request,
    product_id: int,
    data: ProductFullUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can update products."
        )

    product = await update_product_service(db, product_id, data.product)

    if data.variant_categories and data.product.has_variants:
        for cat_data in data.variant_categories:
            await update_variant_category_service(db, cat_data)

    return product

@router.put("/update-variant/{variant_id}", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def update_variant(
    request: Request,
    variant_id: int,
    variant_data: VariantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can update variants."
        )


    return await update_variant_service(db, variant_data, variant_id)



@router.delete("/delete-product/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    request: Request,
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can delete products."
        )

    await delete_product_service(db, product_id)
