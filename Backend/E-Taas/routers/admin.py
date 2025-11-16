from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.database import get_db
from dependencies.auth import current_user
from services.admin import add_product_category, add_service_category, approve_seller, get_sellers_applications
from services.auth import create_admin_user
from schemas.auth import AdminRegister
from schemas.category import ProductCategoryCreate, ServiceCategoryCreate
from models.users import User
from dependencies.limiter import limiter

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def register_admin(
    request: Request,
    admin_data: AdminRegister,
    db: AsyncSession = Depends(get_db),
):
    """Register a new admin. Only run once by the deverloper."""
    return await create_admin_user(db, admin_data)
  

@router.post("/add-product-category", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_product_category(
    request: Request,
    category: ProductCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Add a new product category. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return await add_product_category(db, category)

@router.post("/add-service-category", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_service_category(
    request: Request,
    category: ServiceCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Add a new service category. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return await add_service_category(db, category)


@router.get("/seller-applications", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def manage_sellers_application(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Get all seller applications. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return await get_sellers_applications(db)


@router.put("/verify-seller", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def verify_seller(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Approve a seller. Admin only."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return await approve_seller(db, user_id)
