from fastapi import HTTPException, status, APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from services.products import get_product_by_id, get_all_products, add_product_service, add_product_images, update_product_service, add_variant_categories_with_attributes, add_product_variants, update_variant_category_service, update_variant_service, delete_product_service
from schemas.product import ProductFullCreate, ProductFullUpdate, VariantUpdate
from fastapi import Form, File, UploadFile
from models.users import User

from dependencies.database import get_db
from dependencies.auth import current_user
from dependencies.limiter import limiter

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


@router.post("/add-product", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def add_product_route(
    request: Request,
    data: str = Form(...),
    product_images: list[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can add products."
        )

    parsed_data = ProductFullCreate.parse_raw(data)

    product = await add_product_service(db, parsed_data.product, parsed_data.product.seller_id)
    
    if product_images:
        await add_product_images(db, product.id, product_images)

    if parsed_data.product.has_variants:
        if not parsed_data.variant_categories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Variant categories are required."
            )

        await add_variant_categories_with_attributes(db, parsed_data.variant_categories, product.id)

        await add_product_variants(db, parsed_data.variants, product.id)

    return product


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
    variant_data: str = Form(...),
    variant_image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can update variants."
        )

    parsed_variant_data = VariantUpdate.parse_raw(variant_data)

    return await update_variant_service(db, parsed_variant_data, variant_id, variant_image)



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
